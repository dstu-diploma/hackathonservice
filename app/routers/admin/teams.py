from typing import cast
from app.services.hackathon_teams.dto import HackathonTeamScoreDto
from app.ports.teamservice.dto import HackathonTeamWithMatesDto
from app.dependencies import get_hackathon_teams_service
from app.services.auth.dto import AccessJWTPayloadDto
from app.services.auth import PermittedAction
from app.acl.permissions import Permissions
from fastapi import APIRouter, Depends

from app.routers.admin.dto import CriterionScoreDto
from app.services.hackathon_teams.interface import IHackathonTeamsService

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
    hackathon_teams_service: IHackathonTeamsService = Depends(
        get_hackathon_teams_service
    ),
):
    """
    Возвращает полную информацию о команде-участнике хакатона.
    """
    return await hackathon_teams_service.get_team_info(hackathon_id, team_id)


@router.get(
    "/{hackathon_id}/{team_id}/score",
    response_model=list[HackathonTeamScoreDto],
    summary="Получение списка оценок",
)
async def get_hackathon_team_score(
    hackathon_id: int,
    team_id: int,
    _=Depends(PermittedAction(Permissions.ReadTeamScores)),
    hackathon_teams_service: IHackathonTeamsService = Depends(
        get_hackathon_teams_service
    ),
):
    """
    Возвращает все оценки команды от всех членов жюри, по каждому критериев.
    Не гарантирует, что здесь присутствуют все жюри или все критерии (жюри может не дать оценку по какому-либо хакатону).
    """
    return await hackathon_teams_service.get_all_team_scores(team_id)


@router.get(
    "/{hackathon_id}/{team_id}/score/my",
    response_model=list[HackathonTeamScoreDto],
    summary="Получение моего списка оценок",
)
async def get_hackathon_team_score_by_user(
    hackathon_id: int,
    team_id: int,
    judge_user_dto: AccessJWTPayloadDto = Depends(
        PermittedAction(Permissions.ReadTeamScores)
    ),
    hackathon_teams_service: IHackathonTeamsService = Depends(
        get_hackathon_teams_service
    ),
):
    """
    Возвращает все оценки команды от текущего пользователя по каждому из критериев.
    """
    scores = await hackathon_teams_service.get_all_team_scores(team_id)
    return list(
        filter(
            lambda score: cast(HackathonTeamScoreDto, score).judge_user_id
            == judge_user_dto.user_id,
            scores,
        )
    )


@router.put(
    "/{hackathon_id}/{team_id}/score",
    response_model=HackathonTeamScoreDto,
    summary="Оценка команды",
)
async def set_hackathon_team_score(
    hackathon_id: int,
    team_id: int,
    dto: CriterionScoreDto,
    judge_user_dto: AccessJWTPayloadDto = Depends(
        PermittedAction(Permissions.CreateTeamScore)
    ),
    hackathon_teams_service: IHackathonTeamsService = Depends(
        get_hackathon_teams_service
    ),
):
    """
    Устанавливает оценку от лица жюри (текущего пользователя) по заданному критерию.
    """
    return await hackathon_teams_service.set_score(
        hackathon_id,
        team_id,
        judge_user_dto.user_id,
        dto.criterion_id,
        dto.score,
    )
