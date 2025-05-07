from app.controllers.user import IUserController, get_user_controller
from app.controllers.user.exceptions import UserDoesNotExistException
from app.models.hackathon import HackathonJudgeModel
from functools import lru_cache
from typing import Protocol
from fastapi import Depends
from .dto import JudgeDto

from app.controllers.hackathon import (
    IHackathonController,
    get_hackathon_controller,
)

from .exceptions import (
    HackathonJudgeAlreadyExistsException,
    HackathonJudgeCantManageDateExpiredException,
    HackathonJudgeDoesNotExistsException,
)


class IJudgeController(Protocol):
    user_controller: IUserController
    hackathon_controller: IHackathonController

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


class JudgeController(IJudgeController):
    user_controller: IUserController
    hackathon_controller: IHackathonController

    def __init__(
        self,
        user_controller: IUserController,
        hackathon_controller: IHackathonController,
    ):
        self.user_controller = user_controller
        self.hackathon_controller = hackathon_controller

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
            await self.hackathon_controller.can_edit_hackathon_settings(
                hackathon_id
            )
        ).can_edit

    async def add_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto:
        if not await self._can_manage(hackathon_id):
            raise HackathonJudgeCantManageDateExpiredException()

        if not await self.user_controller.get_user_exists(judge_user_id):
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


@lru_cache
def get_judge_controller(
    user_controller: IUserController = Depends(get_user_controller),
    hackathon_controller: IHackathonController = Depends(
        get_hackathon_controller
    ),
) -> JudgeController:
    return JudgeController(user_controller, hackathon_controller)
