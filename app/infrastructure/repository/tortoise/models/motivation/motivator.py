from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class MotivatorModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    type = fields.CharField(max_length=32, index=True)
    title = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)
    image_url = fields.CharField(max_length=1024, null=True)
    video_url = fields.CharField(max_length=1024, null=True)
    external_url = fields.CharField(max_length=1024, null=True)
    created_by = fields.IntField(index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "motivators"

