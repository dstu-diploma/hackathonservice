from app.controllers.hackathon.dto import HackathonDto
from app.controllers.team.dto import HackathonTeamDto
from app.views.root.dto import TotalHackathonDto
from fastapi import APIRouter, Depends

from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)
from app.controllers.hackathon_teams import (
    get_hackathon_teams_controller,
    HackathonTeamsController,
)

router = APIRouter(tags=["Основное"], prefix="")


@router.get(
    "/",
    response_model=list[HackathonDto],
    summary="Список всех хакатонов",
)
async def get_all(
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Возвращает список всех зарегистрированных хакатонов. О каждом хакатоне предоставляется только общая информация.
    """
    return await hackathon_controller.get_all()


@router.get(
    "/{hack_id}",
    response_model=TotalHackathonDto,
    summary="Детальная информация о хакатоне",
)
async def get_by_id(
    hack_id: int,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает полную информацию о хакатоне. Помимо общей информации (как в `GET /`), здесь перечислены все команды-участники.
    По сути является комбинацией `GET /` и `GET /{hack_id}/teams`.
    """
    hack_data = await hackathon_controller.get(hack_id)
    teams = await hackathon_teams_controller.get_by_hackathon(hack_id)

    return TotalHackathonDto(teams=teams, **hack_data.model_dump())


@router.get(
    "/{hack_id}/teams",
    response_model=list[HackathonTeamDto],
    summary="Список команд-участников хакатона",
)
async def get_teams(
    hack_id: int,
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает список всех команд-участников данного хакатона.
    """
    return await hackathon_teams_controller.get_by_hackathon(hack_id)
