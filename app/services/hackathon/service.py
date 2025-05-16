from tortoise.exceptions import ValidationError, IntegrityError
from app.services.hackathon.interface import IHackathonService
from collections import defaultdict
from tortoise.functions import Sum
from datetime import datetime

from app.services.hackathon.exceptions import (
    HackathonCriteriaCantManageDateExpiredException,
    HackathonCriteriaNameIsNotUniqueException,
    HackathonCriteriaValidationErrorException,
    HackathonCriteriaNotFoundException,
    HackathonValidationErrorException,
    HackathonNameIsNotUniqueException,
    NoSuchHackathonException,
)

from app.services.hackathon.dto import (
    CaEditHackathonSettingsDto,
    CanEditTeamRegistryDto,
    CanGetResultsDto,
    CanMakeScoresDto,
    CanUploadTeamSubmissionsDto,
    OptionalHackathonDto,
    FullHackathonDto,
    HackathonDto,
    CriterionDto,
    TeamScoreDto,
)

from app.models.hackathon import (
    HackathonCriterionModel,
    HackathonModel,
    HackathonTeamFinalScore,
    HackathonTeamScore,
)


class HackathonService(IHackathonService):
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
        now = datetime.now(tz=hackathon.start_date.tzinfo)
        return CanEditTeamRegistryDto(can_edit=now < hackathon.start_date)

    async def can_upload_submissions(
        self, hackathon_id: int
    ) -> CanUploadTeamSubmissionsDto:
        hackathon = await self._get_by_id(hackathon_id)
        now = datetime.now(tz=hackathon.start_date.tzinfo)
        return CanUploadTeamSubmissionsDto(
            can_upload=hackathon.start_date <= now <= hackathon.score_start_date
        )

    async def can_make_scores(self, hackathon_id: int) -> CanMakeScoresDto:
        hackathon = await self._get_by_id(hackathon_id)
        now = datetime.now(tz=hackathon.start_date.tzinfo)

        return CanMakeScoresDto(
            can_make=hackathon.score_start_date <= now <= hackathon.end_date
        )

    async def can_get_results(self, hackathon_id: int) -> CanGetResultsDto:
        hackathon = await self._get_by_id(hackathon_id)
        now = datetime.now(tz=hackathon.start_date.tzinfo)

        return CanGetResultsDto(can_get=hackathon.end_date >= now)

    async def can_edit_hackathon_settings(
        self, hackathon_id: int
    ) -> CaEditHackathonSettingsDto:
        hackathon = await self._get_by_id(hackathon_id)
        now = datetime.now(tz=hackathon.start_date.tzinfo)

        return CaEditHackathonSettingsDto(can_edit=now <= hackathon.start_date)

    async def _can_manage_criterion(self, hackacthon_id: int) -> bool:
        return (await self.can_edit_hackathon_settings(hackacthon_id)).can_edit

    async def add_criterion(
        self, hackathon_id: int, name: str, weight: float
    ) -> CriterionDto:
        if not await self._can_manage_criterion(hackathon_id):
            raise HackathonCriteriaCantManageDateExpiredException()

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

        if not await self._can_manage_criterion(hackathon_id):
            raise HackathonCriteriaCantManageDateExpiredException()

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

        if not await self._can_manage_criterion(hackathon_id):
            raise HackathonCriteriaCantManageDateExpiredException()

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

    async def calculate_team_scores_for_hackathon(
        self, hackathon_id: int, save_to_db: bool = False
    ) -> list[TeamScoreDto]:
        scores = await HackathonTeamScore.filter(
            criterion__hackathon_id=hackathon_id,
            judge__hackathon_id=hackathon_id,
        ).prefetch_related("criterion", "judge")

        if not scores:
            return []

        team_judge_scores: defaultdict[
            int, defaultdict[int, list[tuple[int, float]]]
        ] = defaultdict(lambda: defaultdict(list))

        for score in scores:
            team_judge_scores[score.team_id][score.judge_id].append(  # type: ignore[attr-defined]
                (score.score, score.criterion.weight)
            )

        team_final_scores = {}

        for team_id, judges in team_judge_scores.items():
            judge_totals = []
            for evaluations in judges.values():
                sj = sum(s * w for s, w in evaluations)
                judge_totals.append(sj)
            final_score = sum(judge_totals) / len(judge_totals)
            team_final_scores[team_id] = final_score

            if save_to_db:
                await HackathonTeamFinalScore.update_or_create(
                    {"score": final_score},
                    team_id=team_id,
                )

        return [
            TeamScoreDto(team_id=team_id, score=team_final_scores[team_id])
            for team_id in team_final_scores
        ]
