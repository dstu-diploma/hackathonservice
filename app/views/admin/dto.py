from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated


class CreateHackathonDto(BaseModel):
    name: str
    start_date: datetime
    score_start_date: datetime
    end_date: datetime


class HackathonTeamScoreDto(BaseModel):
    score: Annotated[int, Field(strict=True, ge=0, le=100)]
