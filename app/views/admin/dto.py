from datetime import datetime
from pydantic import BaseModel


class CreateHackathonDto(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime


class TeamIdDto(BaseModel):
    team_id: int
