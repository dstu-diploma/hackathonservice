from app.controllers.hackathon.dto import CriterionDto
from app.routers.admin.dto import CreateCriterionDto
from app.controllers.auth import PermittedAction
from app.acl.permissions import Permissions
from fastapi import APIRouter, Depends

from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)


router = APIRouter(tags=["Управление критериями"], prefix="/criterion")


@router.get(
    "/{hackathon_id}",
    response_model=list[CriterionDto],
    summary="Получение информации о критериях",
)
async def get_hackathon_criteria(
    hackathon_id: int,
    _=Depends(PermittedAction(Permissions.ReadAdminHackathonCriteria)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Возвращает список всех критериев хакатона.
    """
    return await hackathon_controller.get_criteria(hackathon_id)


@router.post(
    "/{hackathon_id}",
    response_model=CriterionDto,
    summary="Создание критерия",
)
async def create_new_criterion(
    hackathon_id: int,
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
        hackathon_id, dto.name, dto.weight
    )


@router.put(
    "/{hackathon_id}/{criterion_id}",
    response_model=CriterionDto,
    summary="Обновление критерия",
)
async def update_existing_criterion(
    hackathon_id: int,
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
        hackathon_id, criterion_id, dto.name, dto.weight
    )


@router.delete(
    "/{hackathon_id}/{criterion_id}",
    response_model=CriterionDto,
    summary="Удаление критерия",
)
async def delete_criterion(
    hackathon_id: int,
    criterion_id: int,
    _=Depends(PermittedAction(Permissions.DeleteCriterion)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Удаляет существующий критерий.
    """
    return await hackathon_controller.delete_criterion(
        hackathon_id, criterion_id
    )
