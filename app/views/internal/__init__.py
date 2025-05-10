from fastapi import APIRouter, Depends, UploadFile
from .auth import get_token_from_header
import io

from app.controllers.hackathon_teams.dto import (
    HackathonTeamSubmissionDto,
)
from app.controllers.hackathon_teams import (
    get_hackathon_teams_controller,
    IHackathonTeamsController,
)

from app.controllers.hackathon import (
    get_hackathon_controller,
    IHackathonController,
)

router = APIRouter(
    tags=["Internal"], prefix="/internal", include_in_schema=False
)


@router.get("/{id}")
async def get_by_hackathon_id(
    id: int,
    _token: str = Depends(get_token_from_header),
    controller: IHackathonController = Depends(get_hackathon_controller),
):
    return await controller.get(id)


@router.get("/{id}/can-edit-team-registry")
async def get_can_edit_team_registry(
    id: int,
    _token: str = Depends(get_token_from_header),
    controller: IHackathonController = Depends(get_hackathon_controller),
):
    return await controller.can_edit_team_registry(id)


@router.put(
    "/{id}/submission/{team_id}",
    response_model=HackathonTeamSubmissionDto,
)
async def upload_submission(
    id: int,
    team_id: int,
    file: UploadFile,
    _token: str = Depends(get_token_from_header),
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    return await hackathon_teams_controller.upload_team_submission(
        id, team_id, io.BytesIO(await file.read())
    )
