from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class CalendarItemModel(BaseTortoiseModel):
    idea_id = fields.IntField(index=True)
    type = fields.CharField(max_length=32, index=True)
    ref_id = fields.IntField(index=True)
    start_datetime = fields.DatetimeField(index=True)
    end_datetime = fields.DatetimeField(index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "calendar_items"

