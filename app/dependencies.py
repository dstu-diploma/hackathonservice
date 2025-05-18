from app.adapters.event_publisher.aiopika import AioPikaEventPublisherAdapter
from app.adapters.event_consumer.aiopika import AioPikaEventConsumerAdapter
from app.services.hackathon_files.interface import IHackathonFilesService
from app.services.hackathon_teams.interface import IHackathonTeamsService
from app.services.hackathon_files.service import HackathonFilesService
from app.services.hackathon_teams.service import HackathonTeamsService
from app.services.hackathon.interface import IHackathonService
from app.services.hackathon.service import HackathonService
from app.ports.event_publisher import IEventPublisherPort
from app.adapters.userservice import UserServiceAdapter
from app.adapters.teamservice import TeamServiceAdapter
from app.ports.event_consumer import IEventConsumerPort
from app.services.judge.interface import IJudgeService
from app.services.judge.service import JudgeService
from app.ports.teamservice import ITeamServicePort
from app.ports.userservice import IUserServicePort
from app.adapters.storage import S3StorageAdapter
from app.ports.storage import IStoragePort
from functools import lru_cache
from app.config import Settings
from fastapi import Depends
import httpx


async def get_http_client():
    return httpx.AsyncClient()


@lru_cache
def get_event_publisher() -> IEventPublisherPort:
    return AioPikaEventPublisherAdapter(Settings.RABBITMQ_URL, "events")


@lru_cache
def get_event_consumer() -> IEventConsumerPort:
    return AioPikaEventConsumerAdapter(
        Settings.RABBITMQ_URL, "events", queue_name="hackathonservice"
    )


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


@lru_cache
def get_hackathon_service(
    event_publisher: IEventPublisherPort = Depends(get_event_publisher),
) -> IHackathonService:
    return HackathonService(event_publisher)


@lru_cache
def get_judge_service(
    user_service: IUserServicePort = Depends(get_user_service),
    hackathon_service: IHackathonService = Depends(get_hackathon_service),
    event_consumer: IEventConsumerPort = Depends(get_event_consumer),
) -> IJudgeService:
    return JudgeService(user_service, hackathon_service, event_consumer)


@lru_cache
def get_hackathon_teams_service(
    hack_service: IHackathonService = Depends(get_hackathon_service),
    team_service: ITeamServicePort = Depends(get_team_service),
    judge_service: IJudgeService = Depends(get_judge_service),
    user_service: IUserServicePort = Depends(get_user_service),
) -> IHackathonTeamsService:
    return HackathonTeamsService(
        hack_service,
        team_service,
        judge_service,
        user_service,
    )


@lru_cache
def get_hackathon_files_service(
    storage: IStoragePort = Depends(get_storage),
) -> IHackathonFilesService:
    return HackathonFilesService("hackathons", storage)
