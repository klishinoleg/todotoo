from dataclasses import dataclass
from datetime import datetime

from core.enums.app.calendar.calendar_item_type import CalendarItemTypeEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class CalendarItemEntity(BaseEntity, TimestampMixin):
    idea_id: int
    type: CalendarItemTypeEnum
    ref_id: int
    start_datetime: datetime
    end_datetime: datetime

