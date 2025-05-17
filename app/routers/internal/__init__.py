from app.services.hackathon.interface import IHackathonService
from app.dependencies import get_hackathon_service
from .auth import get_token_from_header
from fastapi import APIRouter, Depends

router = APIRouter(
    tags=["Internal"], prefix="/internal", include_in_schema=False
)


@router.get("/{id}")
async def get_by_hackathon_id(
    id: int,
    _: str = Depends(get_token_from_header),
    service: IHackathonService = Depends(get_hackathon_service),
):
    return await service.get(id)


@router.post("/info-many")
async def get_info_many(
    hackathon_ids: list[int],
    _: str = Depends(get_token_from_header),
    service: IHackathonService = Depends(get_hackathon_service),
):
    return await service.get_many(hackathon_ids)


@router.get("/{id}/can-edit-team-registry")
async def get_can_edit_team_registry(
    id: int,
    _: str = Depends(get_token_from_header),
    service: IHackathonService = Depends(get_hackathon_service),
):
    return await service.can_edit_team_registry(id)


@router.get("/{id}/can-upload-submissions")
async def get_can_upload_submissions(
    id: int,
    _: str = Depends(get_token_from_header),
    service: IHackathonService = Depends(get_hackathon_service),
):
    return await service.can_upload_submissions(id)
