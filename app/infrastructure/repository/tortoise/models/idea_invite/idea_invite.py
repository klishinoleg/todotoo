from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class IdeaInviteModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    email = fields.CharField(max_length=320, index=True)
    role = fields.CharField(max_length=32, default="contributor")
    message = fields.TextField(null=True)
    token = fields.CharField(max_length=255, unique=True, index=True)
    status = fields.CharField(max_length=32, default="pending", index=True)
    created_by = fields.IntField(index=True)
    accepted_by = fields.IntField(null=True)
    expires_at = fields.DatetimeField(index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    accepted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "idea_invites"

