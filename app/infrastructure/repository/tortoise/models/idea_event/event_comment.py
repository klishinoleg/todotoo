from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class IdeaEventCommentModel(BaseTortoiseModel):
    event_id = fields.IntField(index=True)
    account_id = fields.IntField(index=True)
    text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "idea_event_comments"

