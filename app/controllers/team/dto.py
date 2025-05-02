from pydantic import BaseModel


class HackathonTeamDto(BaseModel):
    id: int
    hackathon_id: int
    name: str


class HackathonTeamMateDto(BaseModel):
    team_id: int
    user_id: int
    is_captain: bool


class HackathonTeamWithMatesDto(HackathonTeamDto):
    mates: list[HackathonTeamMateDto]
