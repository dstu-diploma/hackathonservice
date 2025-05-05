from app.controllers.auth.permissions import Permissions
from app.views.admin.dto import CreateHackathonDto
from app.controllers.auth import PermittedAction
from fastapi import APIRouter, Depends

from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)

from app.controllers.hackathon.dto import (
    OptionalHackathonDto,
    HackathonDto,
)


router = APIRouter(tags=["Управление хакатонами"], prefix="/hackathon")


@router.post(
    "/",
    response_model=HackathonDto,
    summary="Создание хакатона",
)
async def create_hackathon(
    dto: CreateHackathonDto,
    _=Depends(PermittedAction(Permissions.CreateHackathon)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Регистрирует новый хакатон. Имя хакатона должно быть уникальным.
    """
    return await hackathon_controller.create(
        name=dto.name,
        max_participant_count=dto.max_participant_count,
        max_team_mates_count=dto.max_team_mates_count,
        description=dto.description,
        start_date=dto.start_date,
        score_start_date=dto.score_start_date,
        end_date=dto.end_date,
    )


@router.delete(
    "/{hackathon_id}",
    summary="Удаление хакатона",
)
async def delete_hackathon(
    hackathon_id: int,
    _=Depends(PermittedAction(Permissions.DeleteHackathon)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Полностью удаляет данные о хакатоне.
    """
    return await hackathon_controller.delete(hackathon_id)


@router.patch(
    "/{hackathon_id}",
    response_model=HackathonDto,
    summary="Обновление информации о хакатоне",
)
async def update_hackathon_data(
    hackathon_id: int,
    dto: OptionalHackathonDto,
    _=Depends(PermittedAction(Permissions.UpdateHackathon)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Позволяет обновить одно или несколько полей о хакатоне. Все поля необязательные.
    """
    return await hackathon_controller.update(hackathon_id, dto)
