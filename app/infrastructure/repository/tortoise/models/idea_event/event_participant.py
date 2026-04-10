from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class IdeaEventParticipantModel(BaseTortoiseModel):
    event_id = fields.IntField(index=True)
    account_id = fields.IntField(index=True)
    status = fields.CharField(max_length=32, default="joined", index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "idea_event_participants"
        unique_together = (("event_id", "account_id"),)

