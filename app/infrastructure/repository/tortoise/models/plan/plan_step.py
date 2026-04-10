from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class PlanStepModel(BaseTortoiseModel):
    plan_id = fields.IntField(index=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    icon = fields.CharField(max_length=255, null=True)
    position = fields.IntField(default=0, index=True)
    status = fields.CharField(max_length=32, default="todo", index=True)
    assigned_to = fields.IntField(null=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "plan_steps"

