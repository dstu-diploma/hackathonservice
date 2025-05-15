from pydantic import BaseModel, Field, StringConstraints
from datetime import datetime
from typing import Annotated


class CreateHackathonDto(BaseModel):
    name: str
    max_participant_count: int
    max_team_mates_count: int
    description: str
    start_date: datetime
    score_start_date: datetime
    end_date: datetime


class JudgeUserIdDto(BaseModel):
    judge_user_id: int


class CreateCriterionDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=100)]
    weight: Annotated[float, Field(gt=0, le=1)]


class CriterionScoreDto(BaseModel):
    criterion_id: int
    score: Annotated[int, Field(ge=0, le=100)]


class HackathonFileIdDto(BaseModel):
    file_id: int
