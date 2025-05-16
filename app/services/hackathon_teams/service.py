from app.services.hackathon_teams.interface import IHackathonTeamsService
from app.services.hackathon.interface import IHackathonService
from app.services.judge.interface import IJudgeService
from app.services.hackathon.dto import TeamScoreDto
from app.ports.teamservice import ITeamServicePort
from pydantic import ValidationError

from app.ports.teamservice.dto import (
    HackathonTeamWithMatesDto,
    HackathonTeamDto,
)

from app.services.hackathon_teams.dto import (
    HackathonTeamScoreDto,
)

from app.models.hackathon import (
    HackathonTeamFinalScore,
    HackathonTeamScore,
)

from app.services.hackathon_teams.exceptions import (
    HackathonTeamCantBeScoredDateExpiredException,
    HackathonTeamAlreadyScoredException,
    HackathonTeamCantGetResultsException,
)

from app.services.hackathon.exceptions import (
    HackathonCriteriaValidationErrorException,
    NoSuchHackathonException,
)


class HackathonTeamsService(IHackathonTeamsService):
    def __init__(
        self,
        hackathon_service: IHackathonService,
        team_service: ITeamServicePort,
        judge_service: IJudgeService,
    ):
        self.hackathon_service = hackathon_service
        self.team_service = team_service
        self.judge_service = judge_service

    async def get_by_hackathon(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]:
        if not await self.hackathon_service.exists(hackathon_id):
            raise NoSuchHackathonException()

        return await self.team_service.get_hackathon_teams(hackathon_id)

    async def get_team_info(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto:
        if not await self.hackathon_service.exists(hackathon_id):
            raise NoSuchHackathonException()

        return await self.team_service.get_hackathon_team(hackathon_id, team_id)

    async def _can_score(self, hackathon_id: int) -> bool:
        dto = await self.hackathon_service.can_make_scores(hackathon_id)
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
        criterion = await self.hackathon_service.get_criterion(criterion_id)
        judge = await self.judge_service.get_judge(hackathon_id, judge_user_id)

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
        if not await self.hackathon_service.can_get_results(hackathon_id):
            raise HackathonTeamCantGetResultsException()

        teams = await self.get_by_hackathon(hackathon_id)
        team_scores = await HackathonTeamFinalScore.filter(
            team_id__in=map(lambda team: team.id, teams)
        ).order_by("-score")

        return [
            TeamScoreDto(team_id=result.team_id, score=result.score)
            for result in team_scores
        ]
