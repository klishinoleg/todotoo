from dataclasses import dataclass
from datetime import datetime

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class IdeaEventEntity(BaseEntity, TimestampMixin):
    idea_id: int
    title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    capacity: int | None = None
    is_free_join: bool = True
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    cover_image: str | None = None
    created_by: int

