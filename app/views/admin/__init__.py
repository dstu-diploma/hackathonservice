from app.controllers.hackathon.dto import HackathonDto, OptionalHackathonDto
from app.controllers.hackathon_teams import (
    IHackathonTeamsController,
    get_hackathon_teams_controller,
)
from app.controllers.team.dto import HackathonTeamWithMatesDto
from app.views.admin.dto import CreateHackathonDto
from app.controllers.auth import UserWithRole
from fastapi import APIRouter, Depends

from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)


router = APIRouter(
    tags=["Админка"],
    prefix="/admin",
)


@router.post(
    "/hackathon",
    response_model=HackathonDto,
    summary="Создание хакатона",
)
async def create_hackathon(
    dto: CreateHackathonDto,
    _=Depends(UserWithRole("admin")),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Регистрирует новый хакатон. Имя хакатона должно быть уникальным.
    """
    return await hackathon_controller.create(
        name=dto.name,
        start_date=dto.start_date,
        max_participant_count=dto.max_participant_count,
        max_team_mates_count=dto.max_team_mates_count,
        score_start_date=dto.score_start_date,
        end_date=dto.end_date,
    )


@router.delete(
    "/hackathon/{hack_id}",
    summary="Удаление хакатона",
)
async def delete_hackathon(
    hack_id: int,
    _=Depends(UserWithRole("admin")),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Полностью удаляет данные о хакатоне.
    """
    return await hackathon_controller.delete(hack_id)


@router.patch(
    "/hackathon/{hack_id}",
    response_model=HackathonDto,
    summary="Обновление информации о хакатоне",
)
async def update_hackathon_data(
    hack_id: int,
    dto: OptionalHackathonDto,
    _=Depends(UserWithRole("admin")),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Позволяет обновить одно или несколько полей о хакатоне. Все поля необязательные.
    """
    return await hackathon_controller.update(hack_id, dto)


@router.get(
    "/hackathon/{hack_id}/teams/{team_id}",
    response_model=HackathonTeamWithMatesDto,
    summary="Получение информации о команде",
)
async def get_hackathon_team_data(
    hack_id: int,
    team_id: int,
    _=Depends(UserWithRole("admin")),
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает полную информацию о команде-участнике хакатона.
    """
    return await hackathon_teams_controller.get_team_info(hack_id, team_id)
