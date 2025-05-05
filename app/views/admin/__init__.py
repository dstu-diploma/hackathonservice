from app.views.admin.dto import CreateCriterionDto, CreateHackathonDto
from app.controllers.team.dto import HackathonTeamWithMatesDto
from app.controllers.auth.permissions import Permissions
from app.controllers.auth import PermittedAction
from fastapi import APIRouter, Depends

from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)

from app.controllers.hackathon.dto import (
    OptionalHackathonDto,
    CriterionDto,
    HackathonDto,
)
from app.controllers.hackathon_teams import (
    get_hackathon_teams_controller,
    IHackathonTeamsController,
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
    "/hackathon/{hack_id}",
    summary="Удаление хакатона",
)
async def delete_hackathon(
    hack_id: int,
    _=Depends(PermittedAction(Permissions.DeleteHackathon)),
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
    _=Depends(PermittedAction(Permissions.UpdateHackathon)),
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
    _=Depends(PermittedAction(Permissions.ReadAdminHackathonTeamMates)),
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает полную информацию о команде-участнике хакатона.
    """
    return await hackathon_teams_controller.get_team_info(hack_id, team_id)


@router.get(
    "/hackathon/{hack_id}/criterion",
    response_model=list[CriterionDto],
    summary="Получение информации о критериях",
)
async def get_hackathon_criteria(
    hack_id: int,
    _=Depends(PermittedAction(Permissions.ReadAdminHackathonCriteria)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Возвращает список всех критериев хакатона.
    """
    return await hackathon_controller.get_criteria(hack_id)


@router.post(
    "/hackathon/{hack_id}/criterion",
    response_model=CriterionDto,
    summary="Создание критерия",
)
async def create_new_criterion(
    hack_id: int,
    dto: CreateCriterionDto,
    _=Depends(PermittedAction(Permissions.CreateCriterion)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Возвращает список всех критериев хакатона.
    """
    return await hackathon_controller.add_criterion(
        hack_id, dto.name, dto.weight
    )


@router.put(
    "/hackathon/{hack_id}/criterion/{criterion_id}",
    response_model=CriterionDto,
    summary="Обновление критерия",
)
async def update_existing_criterion(
    hack_id: int,
    criterion_id: int,
    dto: CreateCriterionDto,
    _=Depends(PermittedAction(Permissions.UpdateCriterion)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Обновляет существующий критерий.
    """
    return await hackathon_controller.update_criterion(
        hack_id, criterion_id, dto.name, dto.weight
    )


@router.delete(
    "/hackathon/{hack_id}/criterion/{criterion_id}",
    response_model=CriterionDto,
    summary="Удаление критерия",
)
async def delete_criterion(
    hack_id: int,
    criterion_id: int,
    _=Depends(PermittedAction(Permissions.DeleteCriterion)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Удаляет существующий критерий.
    """
    return await hackathon_controller.delete_criterion(hack_id, criterion_id)
