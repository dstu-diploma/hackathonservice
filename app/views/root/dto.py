from app.controllers.hackathon_teams.dto import HackathonTeamDto
from app.controllers.hackathon.dto import HackathonDto


class TotalHackathonDto(HackathonDto):
    teams: list[HackathonTeamDto]
