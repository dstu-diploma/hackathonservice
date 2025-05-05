from app.controllers.auth.dto import AccessJWTPayloadDto
from app.controllers.hackathon_teams.dto import HackathonTeamScoreDto
from app.controllers.team.dto import HackathonTeamWithMatesDto
from app.controllers.auth.permissions import Permissions
from app.controllers.auth import PermittedAction
from fastapi import APIRouter, Depends

from app.controllers.hackathon_teams import (
    get_hackathon_teams_controller,
    IHackathonTeamsController,
)
from app.views.admin.dto import CriterionScoreDto

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


@router.get(
    "/{hackathon_id}/{team_id}/score",
    response_model=list[HackathonTeamScoreDto],
    summary="Получение списка оценок",
)
async def get_hackathon_team_score(
    hackathon_id: int,
    team_id: int,
    _=Depends(PermittedAction(Permissions.ReadTeamScores)),
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Возвращает все оценки команды от всех членов жюри, по каждому критериев.
    Не гарантирует, что здесь присутствуют все жюри или все критерии (жюри может не дать оценку по какому-либо хакатону).
    """
    return await hackathon_teams_controller.get_total_team_score(team_id)


@router.post(
    "/{hackathon_id}/{team_id}/score",
    response_model=HackathonTeamScoreDto,
    summary="Оценка команды",
)
async def set_hackathon_team_score(
    hackathon_id: int,
    team_id: int,
    dto: CriterionScoreDto,
    judge_user_dto: AccessJWTPayloadDto = Depends(
        PermittedAction(Permissions.ReadTeamScores)
    ),
    hackathon_teams_controller: IHackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    """
    Устанавливает оценку от лица жюри (текущего пользователя) по заданному критерию.
    """
    return await hackathon_teams_controller.set_score(
        hackathon_id,
        team_id,
        judge_user_dto.user_id,
        dto.criterion_id,
        dto.score,
    )
