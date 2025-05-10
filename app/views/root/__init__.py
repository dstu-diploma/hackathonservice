from app.controllers.hackathon.dto import HackathonDto, TeamScoreDto
from app.controllers.hackathon_files import (
    IHackathonFilesController,
    get_hackathon_files_controller,
)
from app.controllers.judge import IJudgeController, get_judge_controller
from app.controllers.team.dto import HackathonTeamDto
from app.views.root.dto import DetailedHackathonDto
from fastapi import APIRouter, Depends

from app.controllers.hackathon import (
    get_hackathon_controller,
    IHackathonController,
)
from app.controllers.hackathon_teams import (
    get_hackathon_teams_controller,
    IHackathonTeamsController,
)

router = APIRouter(tags=["Основное"], prefix="")


@router.get(
    "/",
    response_model=list[HackathonDto],
    summary="Список всех хакатонов",
)
async def get_all(
    hackathon_controller: IHackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Возвращает список всех зарегистрированных хакатонов. О каждом хакатоне предоставляется только общая информация.
    """
    return await hackathon_controller.get_all()


@router.get(
    "/{hackathon_id}",
    response_model=DetailedHackathonDto,
    summary="Детальная информация о хакатоне",
)
async def get_by_id(
    hackathon_id: int,
    hackathon_controller: IHackathonController = Depends(
        get_hackathon_controller
    ),
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
    judges_controller: IJudgeController = Depends(get_judge_controller),
    files_controller: IHackathonFilesController = Depends(
        get_hackathon_files_controller
    ),
):
    """
    Возвращает полную информацию о хакатоне. Помимо общей информации (как в `GET /`), здесь перечислены все команды-участники.
    По сути является комбинацией `GET /` и `GET /{hackathon_id}/teams`.
    """
    hack_data = await hackathon_controller.get_full_info(hackathon_id)
    teams = await hackathon_teams_controller.get_by_hackathon(hackathon_id)
    judges = await judges_controller.get_judges(hackathon_id)
    uploads = await files_controller.list_files(hackathon_id)

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
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает список всех команд-участников данного хакатона.
    """
    return await hackathon_teams_controller.get_by_hackathon(hackathon_id)


@router.get(
    "/{hackathon_id}/results",
    response_model=list[TeamScoreDto],
    summary="Таблица лидеров",
)
async def get_result_scores(
    hackathon_id: int,
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает таблицу лидеров хакатона (отсортированный список команд по оценкам).
    Если дата окончания хакатона еще не наступила, то вернет 400.
    """
    return await hackathon_teams_controller.get_result_scores(hackathon_id)
