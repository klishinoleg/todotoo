from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class ParticipationRequestModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    account_id = fields.IntField(index=True)
    message = fields.TextField(null=True)
    status = fields.CharField(max_length=32, default="pending", index=True)
    reviewed_by = fields.IntField(null=True)
    reviewed_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "participation_requests"

