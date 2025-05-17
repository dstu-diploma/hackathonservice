from datetime import datetime
from typing import Protocol

from app.services.hackathon.dto import (
    CaEditHackathonSettingsDto,
    CanEditTeamRegistryDto,
    CanGetResultsDto,
    CanMakeScoresDto,
    CanUploadTeamSubmissionsDto,
    CriterionDto,
    FullHackathonDto,
    HackathonDto,
    OptionalHackathonDto,
    TeamScoreDto,
)


class IHackathonService(Protocol):
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
    async def get_many(
        self, hackathon_ids: list[int]
    ) -> list[HackathonDto]: ...
    async def get(self, hackathon_id: int) -> HackathonDto: ...
    async def delete(self, hackathon_id: int) -> None: ...
    async def can_edit_team_registry(
        self, hackathon_id: int
    ) -> CanEditTeamRegistryDto: ...
    async def can_make_scores(self, hackathon_id: int) -> CanMakeScoresDto: ...
    async def can_get_results(self, hackathon_id: int) -> CanGetResultsDto: ...
    async def can_edit_hackathon_settings(
        self, hackathon_id: int
    ) -> CaEditHackathonSettingsDto: ...
    async def can_upload_submissions(
        self, hackathon_id: int
    ) -> CanUploadTeamSubmissionsDto: ...
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
    async def calculate_team_scores_for_hackathon(
        self, hackathon_id: int, save_to_db: bool = False
    ) -> list[TeamScoreDto]: ...
