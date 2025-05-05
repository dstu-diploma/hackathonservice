from pydantic import BaseModel

from app.models.hackathon import HackathonTeamScore


class HackathonTeamScoreDto(BaseModel):
    id: int
    team_id: int
    criterion_id: int
    judge_user_id: int
    score: int

    @staticmethod
    def from_tortoise(score: HackathonTeamScore):
        return HackathonTeamScoreDto(
            id=score.id,
            team_id=score.team_id,
            criterion_id=score.criterion_id,
            judge_user_id=score.judge_id,
            score=score.score,
        )
