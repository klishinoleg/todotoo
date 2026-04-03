from dataclasses import dataclass
from datetime import datetime

from core.enums.app.meeting.meeting_type import MeetingTypeEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class MeetingEntity(BaseEntity, TimestampMixin):
    idea_id: int
    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime
    type: MeetingTypeEnum = MeetingTypeEnum.OFFLINE
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    meeting_url: str | None = None
    created_by: int

