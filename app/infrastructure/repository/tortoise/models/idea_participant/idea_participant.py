from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class IdeaParticipantModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    account_id = fields.IntField(index=True)
    role = fields.CharField(max_length=32, default="viewer")
    status = fields.CharField(max_length=32, default="pending")
    invited_by = fields.IntField(null=True)
    joined_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "idea_participants"
        unique_together = (("idea_id", "account_id"),)

