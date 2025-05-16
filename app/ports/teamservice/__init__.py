from typing import Protocol

from app.ports.teamservice.dto import (
    HackathonTeamDto,
    HackathonTeamWithMatesDto,
)


class ITeamServicePort(Protocol):
    async def get_team_info(self, team_id: int) -> HackathonTeamDto: ...
    async def get_hackathon_teams(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]: ...
    async def get_hackathon_team(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto: ...

    async def try_get_team_info(self, team_id: int) -> HackathonTeamDto | None:
        try:
            return await self.get_team_info(team_id)
        except Exception:
            return None

    async def get_team_exists(self, team_id: int) -> bool:
        return await self.try_get_team_info(team_id) is not None
