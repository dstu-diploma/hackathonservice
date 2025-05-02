from datetime import datetime
from pydantic import BaseModel

from app.models.hackathon import HackathonModel


class HackathonDto(BaseModel):
    id: int
    name: str
    max_participant_count: int

    start_date: datetime
    score_start_date: datetime
    end_date: datetime

    @staticmethod
    def from_tortoise(hackathon: HackathonModel):
        return HackathonDto(
            id=hackathon.id,
            name=hackathon.name,
            max_participant_count=hackathon.max_participant_count,
            start_date=hackathon.start_date,
            score_start_date=hackathon.score_start_date,
            end_date=hackathon.end_date,
        )


class OptionalHackathonDto(BaseModel):
    name: str | None = None
    max_participant_count: int | None = None

    start_date: datetime | None = None
    score_start_date: datetime | None = None
    end_date: datetime | None = None
