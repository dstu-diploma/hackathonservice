from app.controllers.team.dto import HackathonTeamDto, HackathonTeamWithMatesDto
from app.controllers.hackathon.exceptions import NoSuchHackathonException
from functools import lru_cache
from typing import Protocol
from fastapi import Depends

from app.controllers.hackathon import (
    HackathonController,
    IHackathonController,
    get_hackathon_controller,
)
from app.controllers.team import (
    TeamController,
    get_team_controller,
    ITeamController,
)


class IHackathonTeamsController(Protocol):
    hackathon_controller: IHackathonController
    team_controller: ITeamController

    async def get_by_hackathon(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]: ...
    async def get_team_info(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto: ...


class HackathonTeamsController(IHackathonTeamsController):
    def __init__(
        self,
        hackathon_controller: IHackathonController,
        team_controller: ITeamController,
    ):
        self.hackathon_controller = hackathon_controller
        self.team_controller = team_controller

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


@lru_cache
def get_hackathon_teams_controller(
    hack_controller: HackathonController = Depends(get_hackathon_controller),
    team_controller: TeamController = Depends(get_team_controller),
) -> HackathonTeamsController:
    return HackathonTeamsController(hack_controller, team_controller)
