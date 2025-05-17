from app.models.hackathon import HackathonJudgeModel
from pydantic import BaseModel


class JudgeDto(BaseModel):
    id: int
    hackathon_id: int
    user_id: int
    user_name: str | None = None

    @staticmethod
    def from_tortoise(judge: HackathonJudgeModel):
        return JudgeDto(
            id=judge.id, hackathon_id=judge.hackathon_id, user_id=judge.user_id
        )
