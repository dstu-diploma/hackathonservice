from datetime import datetime
from pydantic import BaseModel

from app.models.hackathon import HackathonModel


class HackathonDto(BaseModel):
    id: int
    name: str

    start_date: datetime
    end_date: datetime

    @staticmethod
    def from_tortoise(hackathon: HackathonModel):
        return HackathonDto(
            id=hackathon.id,
            name=hackathon.name,
            start_date=hackathon.start_date,
            end_date=hackathon.end_date,
        )
