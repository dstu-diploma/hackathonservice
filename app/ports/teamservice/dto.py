from datetime import datetime
from pydantic import BaseModel


class HackathonTeamSubmissionDto(BaseModel):
    id: int
    team_id: int
    hackathon_id: int
    name: str
    s3_key: str
    content_type: str
    uploaded_at: datetime
    url: str | None = None


class HackathonTeamDto(BaseModel):
    id: int
    hackathon_id: int
    name: str
    hackathon_name: str | None = None
    submission: HackathonTeamSubmissionDto | None = None


class HackathonTeamMateDto(BaseModel):
    team_id: int
    user_id: int
    user_name: str | None = None
    is_captain: bool
    role_desc: str | None


class HackathonTeamWithMatesDto(HackathonTeamDto):
    mates: list[HackathonTeamMateDto]
