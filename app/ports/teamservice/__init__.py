from app.ports.teamservice.exceptions import TeamServiceError
from collections import defaultdict
from typing import Protocol

from app.ports.teamservice.dto import (
    HackathonTeamWithMatesDto,
    HackathonTeamDto,
)


class ITeamServicePort(Protocol):
    async def get_team_info(self, team_id: int) -> HackathonTeamDto: ...
    async def get_hackathon_teams(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]: ...
    async def get_hackathon_team_info_many(
        self, hackathon_id: int, team_ids: frozenset[int]
    ) -> list[HackathonTeamDto]: ...
    async def get_hackathon_team(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto: ...

    def get_hackathon_team_name_map(
        self, teams: list[HackathonTeamDto]
    ) -> defaultdict[int, str | None]:
        name_map: defaultdict[int, str | None] = defaultdict(lambda: None)

        for team in teams:
            name_map[team.id] = team.name

        return name_map

    async def try_get_team_info(self, team_id: int) -> HackathonTeamDto | None:
        try:
            return await self.get_team_info(team_id)
        except Exception:
            return None

    async def try_get_hackathon_team_info_many(
        self, hackathon_id: int, team_ids: frozenset[int]
    ) -> list[HackathonTeamDto]:
        try:
            return await self.get_hackathon_team_info_many(
                hackathon_id, team_ids
            )
        except TeamServiceError:
            return []

    async def get_team_exists(self, team_id: int) -> bool:
        return await self.try_get_team_info(team_id) is not None
