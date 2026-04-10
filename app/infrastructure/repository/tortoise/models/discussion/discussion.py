from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class DiscussionModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    title = fields.CharField(max_length=255)
    created_by = fields.IntField(index=True)
    context_type = fields.CharField(max_length=64, null=True, index=True)
    context_id = fields.IntField(null=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "discussions"
