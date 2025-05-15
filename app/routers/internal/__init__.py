from .auth import get_token_from_header
from fastapi import APIRouter, Depends

from app.services.hackathon import (
    get_hackathon_controller,
    IHackathonService,
)


router = APIRouter(
    tags=["Internal"], prefix="/internal", include_in_schema=False
)


@router.get("/{id}")
async def get_by_hackathon_id(
    id: int,
    _token: str = Depends(get_token_from_header),
    controller: IHackathonService = Depends(get_hackathon_controller),
):
    return await controller.get(id)


@router.get("/{id}/can-edit-team-registry")
async def get_can_edit_team_registry(
    id: int,
    _token: str = Depends(get_token_from_header),
    controller: IHackathonService = Depends(get_hackathon_controller),
):
    return await controller.can_edit_team_registry(id)


@router.get("/{id}/can-upload-submissions")
async def get_can_upload_submissions(
    id: int,
    _token: str = Depends(get_token_from_header),
    controller: IHackathonService = Depends(get_hackathon_controller),
):
    return await controller.can_upload_submissions(id)
