from app.controllers.hackathon.dto import FullHackathonDto
from app.controllers.judge.dto import JudgeDto
from app.controllers.team.dto import HackathonTeamDto


class DetailedHackathonDto(FullHackathonDto):
    teams: list[HackathonTeamDto]
    judges: list[JudgeDto]
