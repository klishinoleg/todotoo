from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class MeetingParticipantModel(BaseTortoiseModel):
    meeting_id = fields.IntField(index=True)
    account_id = fields.IntField(index=True)
    status = fields.CharField(max_length=32, default="maybe", index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "meeting_participants"
        unique_together = (("meeting_id", "account_id"),)

