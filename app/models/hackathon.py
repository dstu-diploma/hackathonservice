from tortoise.exceptions import ValidationError
from tortoise.signals import pre_save
from tortoise.models import Model
from tortoise import fields


class HackathonModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=40, unique=True)
    # описание обязательное, но для сохранения старых записей делаем default = ''
    description = fields.CharField(max_length=2000, default="")
    max_participant_count = fields.IntField()
    max_team_mates_count = fields.IntField()

    start_date = fields.DatetimeField()
    score_start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()

    criteria: fields.ReverseRelation["HackathonCriterionModel"]
    judges: fields.ReverseRelation["HackathonJudgeModel"]

    async def validate(self):
        if not (self.start_date < self.score_start_date < self.end_date):
            raise ValidationError(
                "Дата начала должна быть самой ранней, а дата окончания самой поздней!"
            )

    class Meta:
        table: str = "hackathons"


class HackathonDocumentModel(Model):
    id = fields.IntField(pk=True)
    hackathon: fields.ForeignKeyRelation[HackathonModel] = (
        fields.ForeignKeyField(
            "models.HackathonModel", related_name="documents"
        )
    )
    name = fields.CharField(max_length=255)
    s3_key = fields.CharField(max_length=1024)
    content_type = fields.CharField(max_length=255)
    uploaded_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "hackathon_documents"


class HackathonCriterionModel(Model):
    id = fields.IntField(pk=True)
    hackathon: fields.ForeignKeyRelation[HackathonModel] = (
        fields.ForeignKeyField("models.HackathonModel", related_name="criteria")
    )
    name = fields.CharField(max_length=100)
    weight = fields.FloatField()

    async def validate(self):
        if not (0 <= self.weight <= 1):
            raise ValidationError("Вес критерия должен быть между 0 и 1")

    class Meta:
        table: str = "hackathon_criteria"
        unique_together = (("hackathon", "name"),)


class HackathonJudgeModel(Model):
    id = fields.IntField(pk=True)
    hackathon: fields.ForeignKeyRelation[HackathonModel] = (
        fields.ForeignKeyField("models.HackathonModel", related_name="judge")
    )
    user_id = fields.IntField()

    class Meta:
        table: str = "hackathon_judges"
        unique_together = (("hackathon", "user_id"),)


class HackathonTeamScore(Model):
    id = fields.IntField(pk=True)
    team_id = fields.IntField()
    criterion: fields.ForeignKeyRelation[HackathonCriterionModel] = (
        fields.ForeignKeyField(
            "models.HackathonCriterionModel", related_name="scores"
        )
    )
    judge: fields.ForeignKeyRelation[HackathonJudgeModel] = (
        fields.ForeignKeyField(
            "models.HackathonJudgeModel", related_name="scores"
        )
    )
    score = fields.IntField()

    async def validate(self):
        if not (0 <= self.score <= 100):
            raise ValidationError("Оценка должна быть между 0 и 100")

    class Meta:
        table: str = "team_scores"
        unique_together = (("team_id", "criterion", "judge"),)


class HackathonTeamFinalScore(Model):
    id = fields.IntField(pk=True)
    team_id = fields.IntField(unique=True)
    score = fields.FloatField()

    class Meta:
        table = "team_final_scores"


class TeamSubmissionModel(Model):
    id = fields.IntField(pk=True)
    team_id = fields.IntField()
    hackathon: fields.ForeignKeyRelation[HackathonModel] = (
        fields.ForeignKeyField(
            "models.HackathonModel", related_name="submissions"
        )
    )
    name = fields.CharField(max_length=255)
    s3_key = fields.CharField(max_length=1024)
    content_type = fields.CharField(max_length=255)
    uploaded_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "team_submissions"
        unique_together = (("team_id", "hackathon"),)


@pre_save(HackathonModel)
async def __validate_hackathon(_, instance: HackathonModel, __, ___) -> None:
    await instance.validate()


@pre_save(HackathonCriterionModel)
async def __validate_criterion(
    _, instance: HackathonCriterionModel, __, ___
) -> None:
    await instance.validate()


@pre_save(HackathonTeamScore)
async def __validate_score(_, instance: HackathonTeamScore, __, ___) -> None:
    await instance.validate()
