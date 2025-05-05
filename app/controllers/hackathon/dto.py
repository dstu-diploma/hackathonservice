from datetime import datetime
from re import L
from pydantic import BaseModel

from app.models.hackathon import HackathonCriterionModel, HackathonModel


class HackathonDto(BaseModel):
    id: int
    name: str
    max_participant_count: int
    max_team_mates_count: int
    description: str

    start_date: datetime
    score_start_date: datetime
    end_date: datetime

    @staticmethod
    def from_tortoise(hackathon: HackathonModel):
        return HackathonDto(
            id=hackathon.id,
            name=hackathon.name,
            max_participant_count=hackathon.max_participant_count,
            max_team_mates_count=hackathon.max_team_mates_count,
            description=hackathon.description,
            start_date=hackathon.start_date,
            score_start_date=hackathon.score_start_date,
            end_date=hackathon.end_date,
        )


class OptionalHackathonDto(BaseModel):
    name: str | None = None
    max_participant_count: int | None = None
    max_team_mates_count: int | None = None
    description: str | None = None

    start_date: datetime | None = None
    score_start_date: datetime | None = None
    end_date: datetime | None = None


class CanEditTeamRegistryDto(BaseModel):
    can_edit: bool


class CriterionDto(BaseModel):
    id: int
    name: str
    weight: float

    @staticmethod
    def from_tortoise(criterion: HackathonCriterionModel):
        return CriterionDto(
            id=criterion.id, name=criterion.name, weight=criterion.weight
        )


class FullHackathonDto(HackathonDto):
    criteria: list[CriterionDto]
