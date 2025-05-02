from app.controllers.hackathon.dto import HackathonDto
from app.controllers.team.dto import HackathonTeamDto


class TotalHackathonDto(HackathonDto):
    teams: list[HackathonTeamDto]
