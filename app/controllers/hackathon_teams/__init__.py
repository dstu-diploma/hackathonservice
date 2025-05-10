from app.controllers.team.dto import HackathonTeamDto, HackathonTeamWithMatesDto
from app.controllers.judge import IJudgeController, get_judge_controller
from app.controllers.s3 import IS3Controller, get_s3_controller
from app.controllers.hackathon.dto import TeamScoreDto
from pydantic import ValidationError
from functools import lru_cache
from fastapi import Depends
from typing import Protocol
from uuid import uuid4
import io

from app.controllers.hackathon_teams.dto import (
    HackathonTeamScoreDto,
    HackathonTeamSubmissionDto,
)

from app.models.hackathon import (
    HackathonTeamFinalScore,
    HackathonTeamScore,
    TeamSubmissionModel,
)

from app.controllers.hackathon_files.exceptions import (
    HackathonFileTypeRestrictedException,
)

from app.controllers.hackathon_teams.exceptions import (
    HackathonTeamCantBeScoredDateExpiredException,
    HackathonTeamAlreadyScoredException,
    HackathonTeamCantGetResultsException,
    HackathonTeamCantUploadSubmissionsException,
)

from app.controllers.hackathon.exceptions import (
    HackathonCriteriaValidationErrorException,
    NoSuchHackathonException,
)

from app.controllers.hackathon_files import (
    get_hackathon_files_controller,
    IHackathonFilesController,
    utils,
)

from app.controllers.hackathon import (
    get_hackathon_controller,
    IHackathonController,
)
from app.controllers.team import (
    get_team_controller,
    ITeamController,
)


class IHackathonTeamsController(Protocol):
    hackathon_controller: IHackathonController
    team_controller: ITeamController
    judge_controller: IJudgeController
    hackathon_files_controller: IHackathonFilesController
    s3_controller: IS3Controller

    async def get_by_hackathon(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]: ...
    async def get_team_info(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto: ...
    async def set_score(
        self,
        hackathon_id: int,
        team_id: int,
        judge_user_id: int,
        criterion_id: int,
        score: int,
    ) -> HackathonTeamScoreDto: ...
    async def get_all_team_scores(
        self, team_id: int
    ) -> list[HackathonTeamScoreDto]: ...
    async def get_result_scores(
        self, hackathon_id: int
    ) -> list[TeamScoreDto]: ...
    async def upload_team_submission(
        self, hackathon_id: int, team_id: int, file: io.BytesIO
    ) -> HackathonTeamSubmissionDto: ...


class HackathonTeamsController(IHackathonTeamsController):
    def __init__(
        self,
        hackathon_controller: IHackathonController,
        judge_controller: IJudgeController,
        team_controller: ITeamController,
        hackathon_files_controller: IHackathonFilesController,
        s3_controller: IS3Controller,
    ):
        self.hackathon_controller = hackathon_controller
        self.team_controller = team_controller
        self.judge_controller = judge_controller
        self.hackathon_files_controller = hackathon_files_controller
        self.s3_controller = s3_controller

    async def get_by_hackathon(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]:
        if not await self.hackathon_controller.exists(hackathon_id):
            raise NoSuchHackathonException()

        return await self.team_controller.get_hackathon_teams(hackathon_id)

    async def get_team_info(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto:
        if not await self.hackathon_controller.exists(hackathon_id):
            raise NoSuchHackathonException()

        return await self.team_controller.get_hackathon_team(
            hackathon_id, team_id
        )

    async def _can_score(self, hackathon_id: int) -> bool:
        dto = await self.hackathon_controller.can_make_scores(hackathon_id)
        return dto.can_make

    async def _get_score(
        self,
        hack_team_id: int,
        judge_user_id: int,
        criterion_id: int,
    ):
        score = await HackathonTeamScore.get_or_none(
            team_id=hack_team_id,
            criterion_id=criterion_id,
            judge_id=judge_user_id,
        )

        return score

    async def set_score(
        self,
        hackathon_id: int,
        team_id: int,
        judge_user_id: int,
        criterion_id: int,
        score: int,
    ) -> HackathonTeamScoreDto:
        if not await self._can_score(hackathon_id):
            raise HackathonTeamCantBeScoredDateExpiredException()

        if await self._get_score(team_id, judge_user_id, criterion_id):
            raise HackathonTeamAlreadyScoredException()

        hack_team = await self.get_team_info(hackathon_id, team_id)
        criterion = await self.hackathon_controller.get_criterion(criterion_id)
        judge = await self.judge_controller.get_judge(
            hackathon_id, judge_user_id
        )

        try:
            record = await HackathonTeamScore.create(
                team_id=hack_team.id,
                criterion_id=criterion.id,
                judge_id=judge.id,
                score=score,
            )
            return HackathonTeamScoreDto.from_tortoise(record)
        except ValidationError as e:
            raise HackathonCriteriaValidationErrorException("\n".join(e.args))

    async def get_all_team_scores(
        self, team_id: int
    ) -> list[HackathonTeamScoreDto]:
        scores = await HackathonTeamScore.filter(team_id=team_id).order_by(
            "judge_id", "criterion_id"
        )

        return [HackathonTeamScoreDto.from_tortoise(score) for score in scores]

    async def get_result_scores(self, hackathon_id: int) -> list[TeamScoreDto]:
        if not await self.hackathon_controller.can_get_results(hackathon_id):
            raise HackathonTeamCantGetResultsException()

        teams = await self.get_by_hackathon(hackathon_id)
        team_scores = await HackathonTeamFinalScore.filter(
            team_id__in=map(lambda team: team.id, teams)
        ).order_by("-score")

        return [
            TeamScoreDto(team_id=result.team_id, score=result.score)
            for result in team_scores
        ]

    async def upload_team_submission(
        self, hackathon_id: int, team_id: int, file: io.BytesIO
    ) -> HackathonTeamSubmissionDto:
        if not await self.hackathon_controller.can_upload_submissions(
            hackathon_id
        ):
            raise HackathonTeamCantUploadSubmissionsException()

        team = await self.get_team_info(hackathon_id, team_id)
        filename = f"{team.name}_{uuid4()}"

        if self.hackathon_files_controller.is_allowed_file(filename, file):
            raise HackathonFileTypeRestrictedException()

        s3_key = f"team_submissions/{hackathon_id}/{team_id}/{filename}"
        content_type = utils.guess_content_type(filename)

        self.s3_controller.upload_file(file, "hackathons", s3_key, content_type)

        submission, _ = await TeamSubmissionModel.update_or_create(
            defaults={
                "name": filename,
                "s3_key": s3_key,
                "content_type": content_type,
            },
            team_id=team_id,
            hackathon_id=hackathon_id,
        )

        return HackathonTeamSubmissionDto.from_tortoise(submission)


@lru_cache
def get_hackathon_teams_controller(
    hack_controller: IHackathonController = Depends(get_hackathon_controller),
    team_controller: ITeamController = Depends(get_team_controller),
    judge_controller: IJudgeController = Depends(get_judge_controller),
    hackathon_files_controller: IHackathonFilesController = Depends(
        get_hackathon_files_controller
    ),
    s3_controller: IS3Controller = Depends(get_s3_controller),
) -> HackathonTeamsController:
    return HackathonTeamsController(
        hack_controller,
        judge_controller,
        team_controller,
        hackathon_files_controller,
        s3_controller,
    )
