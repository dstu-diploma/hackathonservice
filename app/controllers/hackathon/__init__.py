from app.controllers.hackathon.exceptions import (
    NoSuchHackathonException,
    HackathonNameIsNotUniqueException,
)
from app.controllers.hackathon.dto import HackathonDto, OptionalHackathonDto
from app.models.hackathon import HackathonModel
from tortoise.exceptions import IntegrityError
from datetime import datetime
from typing import Protocol
from fastapi import Depends


class IHackathonController(Protocol):
    async def create(
        self, name: str, start_date: datetime, end_date: datetime
    ) -> HackathonDto: ...
    async def update(
        self, hackathon_id: int, update_dto: OptionalHackathonDto
    ) -> HackathonDto: ...
    async def get_all(self) -> list[HackathonDto]: ...
    async def get(self, hackathon_id: int) -> HackathonDto: ...
    async def delete(self, hackathon_id: int) -> None: ...


class HackathonController(IHackathonController):
    def __init__(self):
        pass

    async def create(
        self, name: str, start_date: datetime, end_date: datetime
    ) -> HackathonDto:
        try:
            hackathon = await HackathonModel.create(
                name=name, start_date=start_date, end_date=end_date
            )
        except IntegrityError:
            raise HackathonNameIsNotUniqueException()

        return HackathonDto.from_tortoise(hackathon)

    async def update(
        self, hackathon_id: int, update_dto: OptionalHackathonDto
    ) -> HackathonDto:
        hackathon = await self._get_by_id(hackathon_id)
        hackathon.update_from_dict(update_dto.model_dump(exclude_none=True))

        await hackathon.save()
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


def get_hackathon_controller(
    controller: HackathonController = Depends(),
) -> HackathonController:
    return controller
