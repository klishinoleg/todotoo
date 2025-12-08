from dataclasses import dataclass
from datetime import datetime

from domain.base.entity import BaseEntity


@dataclass(slots=True, kw_only=True)
class EventOccurrenceEntity(BaseEntity):
    event_id: int
    start_at: datetime
    end_at: datetime
    members_count: int = 0
    location_id: int | None = None
    is_canceled: bool = False
    is_finished: bool = False
