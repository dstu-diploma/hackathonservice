from tortoise.models import Model
from tortoise import fields


class HackathonModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=40, unique=True)

    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()

    class Meta:
        table: str = "hackathons"


class HackathonTeamsModel(Model):
    hackathon: fields.ForeignKeyRelation[HackathonModel] = (
        fields.ForeignKeyField(
            model_name="models.HackathonModel",
            related_name="hackathon_teams",
            on_delete=fields.CASCADE,
        )
    )
    team_id = fields.IntField()

    class Meta:
        table: str = "hackathon_teams"
        unique_together = (("hackathon", "team_id"),)
