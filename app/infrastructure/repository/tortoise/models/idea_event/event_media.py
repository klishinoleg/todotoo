from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class IdeaEventMediaModel(BaseTortoiseModel):
    event_id = fields.IntField(index=True)
    type = fields.CharField(max_length=32, index=True)
    url = fields.CharField(max_length=1024)
    preview_url = fields.CharField(max_length=1024, null=True)
    created_by = fields.IntField(index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "idea_event_media"

