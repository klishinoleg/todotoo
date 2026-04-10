from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class IdeaModel(BaseTortoiseModel):
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    slogan = fields.CharField(max_length=500, null=True)
    cover_image = fields.CharField(max_length=1024, null=True)
    creator_id = fields.IntField()
    visibility = fields.CharField(max_length=32, default="public")
    status = fields.CharField(max_length=32, default="draft")
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "ideas"

