from app.controllers.hackathon import HackathonController, IHackathonController
from app.controllers.hackathon.exceptions import NoSuchHackathonException
from app.models.hackathon import HackathonTeamsModel
from .dto import HackathonTeamDto
from typing import Protocol
from fastapi import Depends

from .exceptions import (
    TeamAlreadyParticipatingException,
    TeamIsNotParticipatingException,
)


class IHackathonTeamsController(Protocol):
    hackathon_controller: IHackathonController

    async def get_by_hackathon(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]: ...
    async def get_by_team(self, team_id: int) -> list[HackathonTeamDto]: ...
    async def is_participating(
        self, hackathon_id: int, team_id: int
    ) -> bool: ...
    async def add(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamDto: ...
    async def delete(self, hackathon_id: int, team_id: int) -> None: ...


class HackathonTeamsController(IHackathonTeamsController):
    def __init__(self, hackathon_controller: IHackathonController):
        self.hackathon_controller = hackathon_controller

    async def get_by_hackathon(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]:
        teams = await HackathonTeamsModel.filter(hackathon_id=hackathon_id)
        return [HackathonTeamDto.from_tortoise(team) for team in teams]

    async def get_by_team(self, team_id: int) -> list[HackathonTeamDto]:
        teams = await HackathonTeamsModel.filter(team_id=team_id)
        return [HackathonTeamDto.from_tortoise(team) for team in teams]

    async def _get_by_team_and_hackathon(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamsModel | None:
        return await HackathonTeamsModel.get_or_none(
            hackathon_id=hackathon_id, team_id=team_id
        )

    async def is_participating(self, hackathon_id: int, team_id: int) -> bool:
        return await HackathonTeamsModel.exists(
            hackathon_id=hackathon_id, team_id=team_id
        )

    async def add(self, hackathon_id: int, team_id: int) -> HackathonTeamDto:
        participant_data = await self._get_by_team_and_hackathon(
            hackathon_id=hackathon_id, team_id=team_id
        )

        if not await self.hackathon_controller.get(hackathon_id):
            raise NoSuchHackathonException()

        if participant_data:
            raise TeamAlreadyParticipatingException()

        await HackathonTeamsModel.create(
            hackathon_id=hackathon_id, team_id=team_id
        )
        return HackathonTeamDto(hackathon_id=hackathon_id, team_id=team_id)

    async def delete(self, hackathon_id: int, team_id: int) -> None:
        participant_data = await self._get_by_team_and_hackathon(
            hackathon_id=hackathon_id, team_id=team_id
        )

        if participant_data:
            return await participant_data.delete()

        raise TeamIsNotParticipatingException()


def get_hackathon_teams_controller(
    hack_controller: HackathonController = Depends(),
) -> HackathonTeamsController:
    return HackathonTeamsController(hack_controller)
