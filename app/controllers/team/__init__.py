from .exceptions import TeamServiceError
from fastapi import Depends
from typing import Protocol
from os import environ
import httpx

TEAM_SERVICE_URL = environ.get("TEAM_SERVICE_URL")
TEAM_SERVICE_API_KEY = environ.get("TEAM_SERVICE_API_KEY")


class ITeamController(Protocol):
    async def get_team_exists(self, team_id: int) -> bool: ...


class TeamController(ITeamController):
    def __init__(
        self,
        client: httpx.AsyncClient,
    ):
        self.client = client
        self.base_url = TEAM_SERVICE_URL
        self.headers = {"Authorization": f"Bearer {TEAM_SERVICE_API_KEY}"}

    async def get_team_exists(self, user_id: int) -> bool:
        url = f"{self.base_url}/{user_id}"

        try:
            response = await self.client.get(url, headers=self.headers)
            return response.status_code == 200
        except httpx.HTTPError as e:
            raise TeamServiceError()


async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client


def get_team_controller(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> TeamController:
    return TeamController(client=client)
