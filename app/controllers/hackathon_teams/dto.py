from app.models.hackathon import HackathonTeamsModel
from pydantic import BaseModel


class HackathonTeamDto(BaseModel):
    hackathon_id: int
    team_id: int

    @staticmethod
    def from_tortoise(hackathon_team: HackathonTeamsModel):
        return HackathonTeamDto(
            hackathon_id=hackathon_team.hackathon_id,
            team_id=hackathon_team.team_id,
        )
