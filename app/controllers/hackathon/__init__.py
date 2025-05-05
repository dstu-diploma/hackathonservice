from tortoise.exceptions import ValidationError, IntegrityError
from tortoise.functions import Sum
from functools import lru_cache
from datetime import datetime
from typing import Protocol

from app.controllers.hackathon.exceptions import (
    HackathonCriteriaNameIsNotUniqueException,
    HackathonCriteriaValidationErrorException,
    HackathonCriteriaNotFoundException,
    HackathonValidationErrorException,
    HackathonNameIsNotUniqueException,
    NoSuchHackathonException,
)

from app.controllers.hackathon.dto import (
    CanEditTeamRegistryDto,
    CanMakeScoresDto,
    OptionalHackathonDto,
    FullHackathonDto,
    HackathonDto,
    CriterionDto,
)

from app.models.hackathon import (
    HackathonCriterionModel,
    HackathonModel,
)


class IHackathonController(Protocol):
    async def create(
        self,
        name: str,
        max_participant_count: int,
        max_team_mates_count: int,
        description: str,
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
    async def can_make_scores(self, hackathon_id: int) -> CanMakeScoresDto: ...
    async def add_criterion(
        self, hackathon_id: int, name: str, weight: float
    ) -> CriterionDto: ...
    async def get_criterion(self, criterion_id: int) -> CriterionDto: ...
    async def get_criteria(self, hackathon_id: int) -> list[CriterionDto]: ...
    async def update_criterion(
        self, hackathon_id: int, criterion_id: int, name: str, weight: float
    ) -> CriterionDto: ...
    async def delete_criterion(
        self, hackathon_id: int, criterion_id: int
    ) -> CriterionDto: ...
    async def get_full_info(self, hackathon_id: int) -> FullHackathonDto: ...


class HackathonController(IHackathonController):
    def __init__(self):
        pass

    async def create(
        self,
        name: str,
        max_participant_count: int,
        max_team_mates_count: int,
        description: str,
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
                description=description,
                score_start_date=score_start_date,
                end_date=end_date,
            )
        except IntegrityError:
            raise HackathonNameIsNotUniqueException()
        except ValidationError as e:
            raise HackathonValidationErrorException("\n".join(e.args))

        return HackathonDto.from_tortoise(hackathon)

    async def exists(self, hackathon_id: int) -> bool:
        return await HackathonModel.exists(id=hackathon_id)

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

    async def can_make_scores(self, hackathon_id: int) -> CanMakeScoresDto:
        hackathon = await self._get_by_id(hackathon_id)
        now = datetime.now(tz=hackathon.start_date.tzinfo)

        return CanMakeScoresDto(
            can_make=hackathon.score_start_date <= now <= hackathon.end_date
        )

    async def add_criterion(
        self, hackathon_id: int, name: str, weight: float
    ) -> CriterionDto:
        try:
            await self._validate_criteria_sum(hackathon_id, weight)

            criterion = await HackathonCriterionModel.create(
                hackathon_id=hackathon_id, name=name, weight=weight
            )
        except IntegrityError:
            raise HackathonCriteriaNameIsNotUniqueException()
        except ValidationError as e:
            raise HackathonCriteriaValidationErrorException("\n".join(e.args))

        return CriterionDto.from_tortoise(criterion)

    async def _validate_criteria_sum(
        self, hackathon_id: int, delta: float = 0
    ) -> None:
        sum_result = (
            await HackathonCriterionModel.filter(hackathon_id=hackathon_id)
            .annotate(sum_weight=Sum("weight"))
            .first()
            .values("sum_weight")
        )

        cur_sum = (sum_result["sum_weight"] or 0) + delta
        if cur_sum > 1.01:
            raise HackathonCriteriaValidationErrorException(
                "Сумма критериев должна быть не больше единицы!"
            )

    async def get_criterion(self, criterion_id: int) -> CriterionDto:
        criterion = await HackathonCriterionModel.get_or_none(id=criterion_id)

        if criterion is None:
            raise HackathonCriteriaNotFoundException()

        return CriterionDto.from_tortoise(criterion)

    async def get_criteria(self, hackathon_id: int) -> list[CriterionDto]:
        await self._get_by_id(hackathon_id)

        criteria = await HackathonCriterionModel.filter(
            hackathon_id=hackathon_id
        )

        return [CriterionDto.from_tortoise(criterion) for criterion in criteria]

    async def update_criterion(
        self, hackathon_id: int, criterion_id: int, name: str, weight: float
    ) -> CriterionDto:
        await self._get_by_id(hackathon_id)

        criterion = await HackathonCriterionModel.get_or_none(
            id=criterion_id, hackathon_id=hackathon_id
        )
        if criterion is None:
            raise HackathonCriteriaNotFoundException()

        await self._validate_criteria_sum(
            hackathon_id, weight - criterion.weight
        )

        criterion.name = name
        criterion.weight = weight

        try:
            await criterion.save()
        except IntegrityError:
            raise HackathonCriteriaNameIsNotUniqueException()
        except ValidationError as e:
            raise HackathonCriteriaValidationErrorException("\n".join(e.args))

        return CriterionDto.from_tortoise(criterion)

    async def delete_criterion(
        self, hackathon_id: int, criterion_id: int
    ) -> CriterionDto:
        await self._get_by_id(hackathon_id)

        criterion = await HackathonCriterionModel.get_or_none(
            id=criterion_id, hackathon_id=hackathon_id
        )
        if criterion is None:
            raise HackathonCriteriaNotFoundException()

        await criterion.delete()
        return CriterionDto.from_tortoise(criterion)

    async def get_full_info(self, hackathon_id: int) -> FullHackathonDto:
        hackathon = await self._get_by_id(hackathon_id)
        criteria = await self.get_criteria(hackathon_id)

        hackathon_dto = HackathonDto.from_tortoise(hackathon)
        return FullHackathonDto(**hackathon_dto.model_dump(), criteria=criteria)


@lru_cache
def get_hackathon_controller() -> HackathonController:
    return HackathonController()
