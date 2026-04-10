from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class IdeaActivityModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    account_id = fields.IntField(null=True, index=True)
    type = fields.CharField(max_length=64, index=True)
    payload: dict[str, object] = fields.JSONField(default=dict)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "idea_activities"
