from datetime import datetime
from pydantic import BaseModel

from app.models.hackathon import HackathonTeamScore


class HackathonTeamScoreDto(BaseModel):
    id: int
    team_id: int
    team_name: str | None = None
    criterion_id: int
    judge_user_id: int
    judge_user_name: str | None = None
    score: int

    @staticmethod
    def from_tortoise(score: HackathonTeamScore):
        return HackathonTeamScoreDto(
            id=score.id,
            team_id=score.team_id,
            criterion_id=score.criterion_id,  # type: ignore[attr-defined]
            judge_user_id=score.judge_id,  # type: ignore[attr-defined]
            score=score.score,
        )
