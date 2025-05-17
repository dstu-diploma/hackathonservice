from pydantic import BaseModel


class HackathonTeamDto(BaseModel):
    id: int
    hackathon_id: int
    name: str
    hackathon_name: str | None = None
    submission_url: str | None = None


class HackathonTeamMateDto(BaseModel):
    team_id: int
    user_id: int
    user_name: str | None = None
    is_captain: bool
    role_desc: str | None


class HackathonTeamWithMatesDto(HackathonTeamDto):
    mates: list[HackathonTeamMateDto]
