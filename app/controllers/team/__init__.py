from .dto import HackathonTeamDto, HackathonTeamWithMatesDto
from fastapi import Depends, HTTPException
from .exceptions import TeamServiceError
from functools import lru_cache
from typing import Protocol
from os import environ
import httpx

TEAM_SERVICE_URL = environ.get("TEAM_SERVICE_URL")
TEAM_SERVICE_API_KEY = environ.get("TEAM_SERVICE_API_KEY")


class ITeamController(Protocol):
    async def get_team_exists(self, user_id: int) -> bool: ...
    async def get_hackathon_teams(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]: ...
    async def get_hackathon_team(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto: ...


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

    async def get_hackathon_teams(
        self, hackathon_id: int
    ) -> list[HackathonTeamDto]:
        url = f"{self.base_url}/hackathon/{hackathon_id}/teams"

        try:
            response = await self.client.get(url, headers=self.headers)
            data: dict = response.json()
            if response.status_code == 200:
                return [HackathonTeamDto(**team) for team in data.values()]
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=data.get("detail", "Internal server error"),
                )
        except httpx.HTTPError as e:
            raise TeamServiceError()

    async def get_hackathon_team(
        self, hackathon_id: int, team_id: int
    ) -> HackathonTeamWithMatesDto:
        url = f"{self.base_url}/hackathon/{hackathon_id}/teams/{team_id}"

        try:
            response = await self.client.get(url, headers=self.headers)
            data: dict = response.json()
            if response.status_code == 200:
                return HackathonTeamWithMatesDto(**data)
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=data.get("detail", "Internal server error"),
                )
        except httpx.HTTPError as e:
            raise TeamServiceError()


async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client


@lru_cache
def get_team_controller(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> TeamController:
    return TeamController(client=client)
