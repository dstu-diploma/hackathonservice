from app.controllers.hackathon.dto import FullHackathonDto
from app.controllers.team.dto import HackathonTeamDto


class HackathonWithTeamsDto(FullHackathonDto):
    teams: list[HackathonTeamDto]
