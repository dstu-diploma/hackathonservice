from app.services.hackathon_teams.dto import HackathonTeamScoreDto
from app.services.hackathon.interface import IHackathonService
from app.services.judge.interface import IJudgeService
from app.services.hackathon.dto import TeamScoreDto
from app.ports.teamservice import ITeamServicePort
from typing import Protocol

from app.ports.teamservice.dto import (
    HackathonTeamDto,
    HackathonTeamWithMatesDto,
)


class IHackathonTeamsService(Protocol):
    hackathon_service: IHackathonService
    team_service: ITeamServicePort
    judge_service: IJudgeService

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
