from tortoise.exceptions import ValidationError
from app.models.hackathon import HackathonModel
from tortoise.exceptions import IntegrityError
from functools import lru_cache
from datetime import datetime
from typing import Protocol
from fastapi import Depends

from app.controllers.hackathon.exceptions import (
    HackathonValidationErrorException,
    NoSuchHackathonException,
    HackathonNameIsNotUniqueException,
)
from app.controllers.hackathon.dto import (
    CanEditTeamRegistryDto,
    OptionalHackathonDto,
    HackathonDto,
)


class IHackathonController(Protocol):
    async def create(
        self,
        name: str,
        max_participant_count: int,
        max_team_mates_count: int,
        start_date: datetime,
        score_start_date: datetime,
        end_date: datetime,
    ) -> HackathonDto: ...
    async def exists(self, hackathon_id: int) -> bool: ...
    async def update(
        self, hackathon_id: int, update_dto: OptionalHackathonDto
    ) -> HackathonDto: ...
    async def get_all(self) -> list[HackathonDto]: ...
    async def get(self, hackathon_id: int) -> HackathonDto: ...
    async def delete(self, hackathon_id: int) -> None: ...
    async def can_edit_team_registry(
        self, hackathon_id: int
    ) -> CanEditTeamRegistryDto: ...


class HackathonController(IHackathonController):
    def __init__(self):
        pass

    async def create(
        self,
        name: str,
        max_participant_count: int,
        max_team_mates_count: int,
        start_date: datetime,
        score_start_date: datetime,
        end_date: datetime,
    ) -> HackathonDto:
        try:
            hackathon = await HackathonModel.create(
                name=name,
                start_date=start_date,
                max_participant_count=max_participant_count,
                max_team_mates_count=max_team_mates_count,
                score_start_date=score_start_date,
                end_date=end_date,
            )
        except IntegrityError:
            raise HackathonNameIsNotUniqueException()
        except ValidationError as e:
            raise HackathonValidationErrorException("\n".join(e.args))

        return HackathonDto.from_tortoise(hackathon)

    async def exists(self, hackathon_id: int) -> bool:
        return await HackathonModel.exists(hackathon_id=hackathon_id)

    async def update(
        self, hackathon_id: int, update_dto: OptionalHackathonDto
    ) -> HackathonDto:
        hackathon = await self._get_by_id(hackathon_id)
        hackathon.update_from_dict(update_dto.model_dump(exclude_none=True))

        try:
            await hackathon.save()
        except ValidationError as e:
            raise HackathonValidationErrorException("\n".join(e.args))

        return HackathonDto.from_tortoise(hackathon)

    async def get_all(self) -> list[HackathonDto]:
        hackathons = await HackathonModel.all()
        return [
            HackathonDto.from_tortoise(hackathon) for hackathon in hackathons
        ]

    async def _get_by_id(self, hackathon_id: int) -> HackathonModel:
        hackathon = await HackathonModel.get_or_none(id=hackathon_id)
        if hackathon is None:
            raise NoSuchHackathonException()

        return hackathon

    async def get(self, hackathon_id: int) -> HackathonDto:
        hackathon = await self._get_by_id(hackathon_id)
        return HackathonDto.from_tortoise(hackathon)

    async def delete(self, hackathon_id: int) -> None:
        hackathon = await self._get_by_id(hackathon_id)
        await hackathon.delete()

    async def can_edit_team_registry(
        self, hackathon_id: int
    ) -> CanEditTeamRegistryDto:
        hackathon = await self._get_by_id(hackathon_id)
        return CanEditTeamRegistryDto(
            can_edit=datetime.now(tz=hackathon.start_date.tzinfo)
            < hackathon.start_date
        )


@lru_cache
def get_hackathon_controller() -> HackathonController:
    return HackathonController()
