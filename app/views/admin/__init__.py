from fastapi import APIRouter, Depends

from app.controllers.auth import UserWithRole
from app.controllers.hackathon import (
    HackathonController,
    get_hackathon_controller,
)
from app.controllers.hackathon.dto import HackathonDto, OptionalHackathonDto
from app.controllers.hackathon_teams import (
    HackathonTeamsController,
    get_hackathon_teams_controller,
)
from app.controllers.hackathon_teams.dto import HackathonTeamDto
from app.views.admin.dto import CreateHackathonDto

router = APIRouter(
    tags=["Админка"],
    prefix="/admin",
    dependencies=(Depends(UserWithRole("admin")),),
)


@router.post(
    "/hackathon",
    response_model=HackathonDto,
    summary="Создание хакатона",
    description="Регистрирует новый хакатон. Имя хакатона должно быть уникальным.",
)
async def create_hackathon(
    data: CreateHackathonDto,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.create(
        name=data.name, start_date=data.start_date, end_date=data.end_date
    )


@router.delete(
    "/hackathon/{hack_id}",
    summary="Удаление хакатона",
    description="Полностью удаляет данные о хакатоне",
)
async def delete_hackathon(
    hack_id: int,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.delete(hack_id)


@router.patch(
    "/hackathon/{hack_id}",
    response_model=HackathonDto,
    summary="Обновление информации о хакатоне",
    description="Позволяет обновить одно или несколько полей о хакатоне. Все поля необязательные.",
)
async def update_hackathon_data(
    hack_id: int,
    dto: OptionalHackathonDto,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.update(hack_id, dto)


@router.post(
    "/hackathon/{hack_id}/teams/{team_id}",
    response_model=HackathonTeamDto,
    summary="Добавление команды-участника",
    description="Позволяет зарегистрировать команду как участника данного хакатона. Проводится проверка на существование команды (обращение в TeamService)",
)
async def add_team(
    hack_id: int,
    team_id: int,
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    return await hackathon_teams_controller.add(hack_id, team_id)


@router.delete(
    "/hackathon/{hack_id}/teams/{team_id}",
    summary="Удаление команды-участника",
    description="Позволяет убрать команду как участника хакатона.",
)
async def delete_team(
    hack_id: int,
    team_id: int,
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    return await hackathon_teams_controller.delete(hack_id, team_id)
