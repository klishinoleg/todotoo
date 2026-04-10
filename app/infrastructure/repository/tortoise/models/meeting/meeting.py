from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class MeetingModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    start_datetime = fields.DatetimeField(index=True)
    end_datetime = fields.DatetimeField()
    type = fields.CharField(max_length=32, default="offline", index=True)
    location_name = fields.CharField(max_length=255, null=True)
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)
    meeting_url = fields.CharField(max_length=1024, null=True)
    created_by = fields.IntField(index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "meetings"

