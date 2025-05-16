from app.ports.userservice.exceptions import UserDoesNotExistException
from app.services.hackathon.interface import IHackathonService
from app.services.judge.interface import IJudgeService
from app.models.hackathon import HackathonJudgeModel
from app.ports.userservice import IUserServicePort
from app.services.judge.dto import JudgeDto


from app.services.judge.exceptions import (
    HackathonJudgeAlreadyExistsException,
    HackathonJudgeCantManageDateExpiredException,
    HackathonJudgeDoesNotExistsException,
)


class JudgeService(IJudgeService):
    user_service: IUserServicePort
    hackathon_service: IHackathonService

    def __init__(
        self,
        user_service: IUserServicePort,
        hackathon_service: IHackathonService,
    ):
        self.user_service = user_service
        self.hackathon_service = hackathon_service

    async def _get_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> HackathonJudgeModel:
        judge = await HackathonJudgeModel.get_or_none(
            hackathon_id=hackathon_id, user_id=judge_user_id
        )
        if judge is None:
            raise HackathonJudgeDoesNotExistsException()

        return judge

    async def get_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto:
        judge = await self._get_judge(hackathon_id, judge_user_id)
        return JudgeDto.from_tortoise(judge)

    async def _can_manage(self, hackathon_id: int) -> bool:
        return (
            await self.hackathon_service.can_edit_hackathon_settings(
                hackathon_id
            )
        ).can_edit

    async def add_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto:
        if not await self._can_manage(hackathon_id):
            raise HackathonJudgeCantManageDateExpiredException()

        if not await self.user_service.get_user_exists(judge_user_id):
            raise UserDoesNotExistException()

        if await HackathonJudgeModel.get_or_none(
            hackathon_id=hackathon_id, user_id=judge_user_id
        ):
            raise HackathonJudgeAlreadyExistsException()

        judge = await HackathonJudgeModel.create(
            hackathon_id=hackathon_id, user_id=judge_user_id
        )

        return JudgeDto.from_tortoise(judge)

    async def get_judges(self, hackathon_id: int) -> list[JudgeDto]:
        judges = await HackathonJudgeModel.filter(hackathon_id=hackathon_id)
        return [JudgeDto.from_tortoise(judge) for judge in judges]

    async def delete_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto:
        if not await self._can_manage(hackathon_id):
            raise HackathonJudgeCantManageDateExpiredException()

        judge = await self._get_judge(hackathon_id, judge_user_id)
        await judge.delete()
        return JudgeDto.from_tortoise(judge)
