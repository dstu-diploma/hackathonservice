from app.controllers.team.dto import HackathonTeamWithMatesDto
from app.controllers.auth.permissions import Permissions
from app.controllers.auth import PermittedAction
from fastapi import APIRouter, Depends

from app.controllers.hackathon_teams import (
    get_hackathon_teams_controller,
    IHackathonTeamsController,
)

router = APIRouter(tags=["Управление командами"], prefix="/teams")


@router.get(
    "/{hackathon_id}/{team_id}",
    response_model=HackathonTeamWithMatesDto,
    summary="Получение информации о команде",
)
async def get_hackathon_team_data(
    hackathon_id: int,
    team_id: int,
    _=Depends(PermittedAction(Permissions.ReadAdminHackathonTeamMates)),
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает полную информацию о команде-участнике хакатона.
    """
    return await hackathon_teams_controller.get_team_info(hackathon_id, team_id)
