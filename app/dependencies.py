from functools import lru_cache
from fastapi import Depends
import httpx

from app.adapters.storage import S3StorageAdapter
from app.adapters.teamservice import TeamServiceAdapter
from app.adapters.userservice import UserServiceAdapter
from app.ports.storage import IStoragePort
from app.ports.teamservice import ITeamServicePort
from app.ports.userservice import IUserServicePort


async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client


@lru_cache
def get_team_service(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> ITeamServicePort:
    return TeamServiceAdapter(client)


@lru_cache
def get_user_service(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> IUserServicePort:
    return UserServiceAdapter(client)


@lru_cache
def get_storage() -> IStoragePort:
    return S3StorageAdapter()
