from app.ports.teamservice.exceptions import TeamServiceError
from app.ports.teamservice import ITeamServicePort
from fastapi import HTTPException
from app.config import Settings
import urllib.parse
import httpx

from app.ports.teamservice.dto import (
    HackathonTeamWithMatesDto,
    HackathonTeamDto,
)


class TeamServiceAdapter(ITeamServicePort):
    def __init__(
        self,
        client: httpx.AsyncClient,
    ):
        self.client = client
        self.base_url = Settings.TEAM_SERVICE_URL
        self.headers = {
            "Authorization": f"Bearer {Settings.TEAM_SERVICE_API_KEY}"
        }

    async def _do_get(self, url: str) -> dict:
        try:
            response = await self.client.get(url, headers=self.headers)
            data = response.json()
            if response.status_code == 200:
                return data
            else:
                raise HTTPException(
                    status_code=response.status_code, detail=data["detail"]
                )
        except httpx.HTTPError as e:
            raise TeamServiceError()

    async def get_team_info(self, team_id: int) -> HackathonTeamDto:
        data = await self._do_get(
            urllib.parse.urljoin(self.base_url, str(team_id))
        )
        return HackathonTeamDto(**data)

    async def get_hackathon_teams(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]:
        data = await self._do_get(
            f"{self.base_url}/hackathon/{hackathon_id}/teams"
        )
        return [HackathonTeamDto(**team) for team in data]

    async def get_hackathon_team(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto:
        data = await self._do_get(
            f"{self.base_url}/hackathon/{hackathon_id}/teams/{team_id}"
        )
        return HackathonTeamWithMatesDto(**data)
