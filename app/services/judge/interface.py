from app.ports.userservice import IUserServicePort
from app.services.hackathon.interface import IHackathonService
from app.services.judge.dto import JudgeDto
from typing import Protocol


class IJudgeService(Protocol):
    user_service: IUserServicePort
    hackathon_service: IHackathonService

    async def add_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto: ...
    async def get_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto: ...
    async def get_judges(self, hackathon_id: int) -> list[JudgeDto]: ...
    async def delete_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto: ...
