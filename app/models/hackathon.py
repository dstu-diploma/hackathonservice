from tortoise.exceptions import ValidationError
from tortoise.signals import pre_save
from tortoise.models import Model
from tortoise import fields


class HackathonModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=40, unique=True)
    max_participant_count = fields.IntField()
    max_team_mates_count = fields.IntField()

    start_date = fields.DatetimeField()
    score_start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()

    async def validate(self):
        if not (self.start_date < self.score_start_date < self.end_date):
            raise ValidationError(
                "Дата начала должна быть самой ранней, а дата окончания самой поздней!"
            )

    class Meta:
        table: str = "hackathons"


@pre_save(HackathonModel)
async def __validate_hackathon(_, instance: HackathonModel, __, ___) -> None:
    await instance.validate()
