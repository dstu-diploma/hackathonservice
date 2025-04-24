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
from app.views.admin.dto import CreateHackathonDto, TeamIdDto

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
    "/hackathon/{id}",
    summary="Удаление хакатона",
    description="Полностью удаляет данные о хакатоне",
)
async def delete_hackathon(
    id: int,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.delete(id)


@router.patch(
    "/hackathon/{id}",
    response_model=HackathonDto,
    summary="Обновление информации о хакатоне",
    description="Позволяет обновить одно или несколько полей о хакатоне. Все поля необязательные.",
)
async def update_hackathon_data(
    id: int,
    dto: OptionalHackathonDto,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.update(id, dto)


@router.post(
    "/hackathon/{id}/teams",
    response_model=HackathonTeamDto,
    summary="Добавление команды-участника",
    description="Позволяет зарегистрировать команду как участника данного хакатона. Проводится проверка на существование команды (обращение в TeamService)",
)
async def add_team(
    id: int,
    dto: TeamIdDto,
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    return await hackathon_teams_controller.add(id, dto.team_id)


@router.delete(
    "/hackathon/{id}/teams",
    summary="Удаление команды-участника",
    description="Позволяет убрать команду как участника хакатона.",
)
async def delete_team(
    id: int,
    dto: TeamIdDto,
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    return await hackathon_teams_controller.delete(id, dto.team_id)
