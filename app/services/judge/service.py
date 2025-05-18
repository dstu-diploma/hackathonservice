from app.ports.userservice.exceptions import UserDoesNotExistException
from app.services.hackathon.interface import IHackathonService
from app.ports.event_consumer import IEventConsumerPort
from app.services.judge.interface import IJudgeService
from app.models.hackathon import HackathonJudgeModel
from app.ports.userservice import IUserServicePort
from app.services.judge.dto import JudgeDto
import app.util.dto_utils as dto_utils
from app.events.emitter import Emitter
from app.events.emitter import Events


from app.services.judge.exceptions import (
    HackathonJudgeCantManageDateExpiredException,
    HackathonJudgeAlreadyExistsException,
    HackathonJudgeDoesNotExistsException,
)


class JudgeService(IJudgeService):
    def __init__(
        self,
        user_service: IUserServicePort,
        hackathon_service: IHackathonService,
        event_consumer: IEventConsumerPort,
    ):
        self.user_service = user_service
        self.hackathon_service = hackathon_service
        self.event_consumer = event_consumer

        self._init_events()

    def _init_events(self):
        async def on_user_deleted(payload: dict):
            data: dict | None = payload.get("data", None)
            if data is None:
                return

            user_id = data.get("id")
            if user_id is None:
                return

            await HackathonJudgeModel.filter(user_id=user_id).delete()

        async def on_user_banned(payload: dict):
            is_banned = payload["data"]["is_banned"]
            if is_banned:
                return await on_user_deleted(payload)

        Emitter.on(Events.UserDeleted, on_user_deleted)
        Emitter.on(Events.UserBanned, on_user_banned)

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

        dto = JudgeDto.from_tortoise(judge)
        user_info = await self.user_service.try_get_user_info(judge.user_id)

        if user_info:
            dto.user_name = user_info.formatted_name

        return dto

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

        user_info = await self.user_service.try_get_user_info(judge_user_id)
        if user_info is None:
            raise UserDoesNotExistException()

        if await HackathonJudgeModel.get_or_none(
            hackathon_id=hackathon_id, user_id=judge_user_id
        ):
            raise HackathonJudgeAlreadyExistsException()

        judge = await HackathonJudgeModel.create(
            hackathon_id=hackathon_id, user_id=judge_user_id
        )

        dto = JudgeDto.from_tortoise(judge)
        dto.user_name = user_info.formatted_name

        return dto

    async def get_judges(self, hackathon_id: int) -> list[JudgeDto]:
        judges = await HackathonJudgeModel.filter(hackathon_id=hackathon_id)
        dtos = [JudgeDto.from_tortoise(judge) for judge in judges]
        names = self.user_service.get_name_map(
            await self.user_service.try_get_user_info_many(
                dto_utils.export_int_fields(dtos, "user_id")
            )
        )

        return dto_utils.inject_mapping(
            dtos, names, "user_id", "user_name", strict=True
        )

    async def delete_judge(
        self, hackathon_id: int, judge_user_id: int
    ) -> JudgeDto:
        if not await self._can_manage(hackathon_id):
            raise HackathonJudgeCantManageDateExpiredException()

        judge = await self._get_judge(hackathon_id, judge_user_id)
        await judge.delete()
        return JudgeDto.from_tortoise(judge)
