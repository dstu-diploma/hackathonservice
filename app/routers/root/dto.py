from app.ports.teamservice.dto import HackathonTeamDto
from app.services.hackathon.dto import FullHackathonDto
from app.services.hackathon_files.dto import HackathonDocumentWithLinkDto
from app.services.judge.dto import JudgeDto


class DetailedHackathonDto(FullHackathonDto):
    teams: list[HackathonTeamDto]
    judges: list[JudgeDto]
    uploads: list[HackathonDocumentWithLinkDto]
