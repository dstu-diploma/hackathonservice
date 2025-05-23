from app.models.hackathon import HackathonJudgeModel
from app.ports.userservice.dto import UserUploadDto
from pydantic import BaseModel


class JudgeDto(BaseModel):
    id: int
    hackathon_id: int
    user_id: int
    user_name: str | None = None
    user_uploads: list[UserUploadDto] | None = None

    @staticmethod
    def from_tortoise(judge: HackathonJudgeModel):
        return JudgeDto(
            id=judge.id, hackathon_id=judge.hackathon_id, user_id=judge.user_id
        )
