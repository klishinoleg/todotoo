from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class PlanModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    icon = fields.CharField(max_length=255, null=True)
    position = fields.IntField(default=0, index=True)
    created_by = fields.IntField(index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "plans"

