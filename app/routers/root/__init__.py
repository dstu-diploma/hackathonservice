from app.services.hackathon.dto import CriterionDto, HackathonDto, TeamScoreDto
from app.services.hackathon_teams.interface import IHackathonTeamsService
from app.services.hackathon_files.interface import IHackathonFilesService
from app.services.hackathon.interface import IHackathonService
from app.ports.teamservice.dto import HackathonTeamDto
from app.services.judge.interface import IJudgeService
from app.routers.root.dto import DetailedHackathonDto
from fastapi import APIRouter, Depends, Request
from app.config import Settings

from app.dependencies import (
    get_hackathon_files_service,
    get_hackathon_teams_service,
    get_hackathon_service,
    get_judge_service,
)
from app.services.judge.dto import JudgeDto

router = APIRouter(tags=["Основное"], prefix="")


@router.get(
    "/",
    response_model=list[HackathonDto],
    summary="Список всех хакатонов",
)
async def get_all(
    hackathon_service: IHackathonService = Depends(get_hackathon_service),
):
    """
    Возвращает список всех зарегистрированных хакатонов. О каждом хакатоне предоставляется только общая информация.
    """
    return await hackathon_service.get_all()


@router.get(
    "/{hackathon_id}",
    response_model=DetailedHackathonDto,
    summary="Детальная информация о хакатоне",
)
async def get_by_id(
    hackathon_id: int,
    request: Request,
    hackathon_service: IHackathonService = Depends(get_hackathon_service),
    hackathon_teams_service: IHackathonTeamsService = Depends(
        get_hackathon_teams_service
    ),
    judges_service: IJudgeService = Depends(get_judge_service),
    files_service: IHackathonFilesService = Depends(
        get_hackathon_files_service
    ),
):
    """
    Возвращает полную информацию о хакатоне. Помимо общей информации (как в `GET /`), здесь перечислены все команды-участники.
    По сути является комбинацией `GET /` и `GET /{hackathon_id}/teams`.
    """
    hack_data = await hackathon_service.get_full_info(hackathon_id)
    teams = await hackathon_teams_service.get_by_hackathon(hackathon_id)
    judges = await judges_service.get_judges(hackathon_id)
    uploads = await files_service.get_files(
        hackathon_id,
        Settings.PUBLIC_API_URL or str(request.base_url).rstrip("/"),
    )

    return DetailedHackathonDto(
        teams=teams, judges=judges, uploads=uploads, **hack_data.model_dump()
    )


@router.get(
    "/{hackathon_id}/teams",
    response_model=list[HackathonTeamDto],
    summary="Список команд-участников хакатона",
)
async def get_teams(
    hackathon_id: int,
    hackathon_teams_service: IHackathonTeamsService = Depends(
        get_hackathon_teams_service
    ),
):
    """
    Возвращает список всех команд-участников данного хакатона.
    """
    return await hackathon_teams_service.get_by_hackathon(hackathon_id)


@router.get(
    "/{hackathon_id}/results",
    response_model=list[TeamScoreDto],
    summary="Таблица лидеров",
)
async def get_result_scores(
    hackathon_id: int,
    hackathon_teams_service: IHackathonTeamsService = Depends(
        get_hackathon_teams_service
    ),
):
    """
    Возвращает таблицу лидеров хакатона (отсортированный список команд по оценкам).
    Если дата окончания хакатона еще не наступила, то вернет 400.
    """
    return await hackathon_teams_service.get_result_scores(hackathon_id)


@router.get(
    "/{hackathon_id}/criteria",
    response_model=list[CriterionDto],
    summary="Список критериев",
)
async def get_criteria(
    hackathon_id: int,
    hackathon_service: IHackathonService = Depends(get_hackathon_service),
):
    """
    Возвращает список критериев оценивания хакатона.
    """
    return await hackathon_service.get_criteria(hackathon_id)


@router.get(
    "/{hackathon_id}/judges",
    response_model=list[JudgeDto],
    summary="Члены жюри",
)
async def get_judges(
    hackathon_id: int,
    judges_service: IJudgeService = Depends(get_judge_service),
):
    """
    Возвращает список судей хакатона.
    """
    return await judges_service.get_judges(hackathon_id)
