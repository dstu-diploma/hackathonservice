from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)
from app.controllers.hackathon_teams import (
    get_hackathon_teams_controller,
    HackathonTeamsController,
)

from app.controllers.hackathon_teams.dto import HackathonTeamDto
from app.views.root.dto import TotalHackathonDto
from fastapi import APIRouter, Depends


router = APIRouter(tags=["Основное"], prefix="")


@router.get("/")
async def get_all(
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.get_all()


@router.get("/{id}", response_model=TotalHackathonDto)
async def get_by_id(
    id: int,
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    hack_data = await hackathon_controller.get(id)
    teams = await hackathon_teams_controller.get_by_hackathon(id)

    return TotalHackathonDto(teams=teams, **hack_data.model_dump())


@router.get("/{id}/teams", response_model=list[HackathonTeamDto])
async def get_teams(
    id: int,
    hackathon_teams_controller: HackathonTeamsController = Depends(
        get_hackathon_teams_controller
    ),
):
    return await hackathon_teams_controller.get_by_hackathon(id)
