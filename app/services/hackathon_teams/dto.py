from app.models.hackathon import HackathonTeamScore
from pydantic import BaseModel


class HackathonTeamScoreDto(BaseModel):
    id: int
    team_id: int
    team_name: str | None = None
    criterion_id: int
    judge_user_id: int
    judge_user_name: str | None = None
    score: int

    @staticmethod
    def from_tortoise(score: HackathonTeamScore, judge_user_id: int):
        return HackathonTeamScoreDto(
            id=score.id,
            team_id=score.team_id,
            criterion_id=score.criterion_id,  # type: ignore[attr-defined]
            judge_user_id=judge_user_id,
            score=score.score,
        )
