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
    summary="Список всех хакатонов",
    description="Возвращает список всех зарегистрированных хакатонов. О каждом хакатоне предоставляется только общая информация.",
)
async def get_all(
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.get_all()


@router.get(
    "/{id}",
    response_model=TotalHackathonDto,
    summary="Детальная информация о хакатоне",
    description="Возвращает полную информацию о хакатоне. Помимо общей информации (как в `GET /`), здесь перечислены все команды-участники. По сути является комбинацией `GET /` и `GET /{id}/teams`.",
)
async def get_by_id(
    id: int,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    hack_data = await hackathon_controller.get(id)
    teams = await hackathon_teams_controller.get_by_hackathon(id)

    return TotalHackathonDto(teams=teams, **hack_data.model_dump())


@router.get(
    "/{id}/teams",
    response_model=list[HackathonTeamDto],
    summary="Список команд-участников хакатона",
    description="Возвращает список всех команд-участников данного хакатона.",
)
async def get_teams(
    id: int,
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    return await hackathon_teams_controller.get_by_hackathon(id)
