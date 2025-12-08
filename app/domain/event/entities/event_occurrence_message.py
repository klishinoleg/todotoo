from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin
from domain.base.mixins.with_active import WithActiveMixin


@dataclass(slots=True, kw_only=True)
class EventOccurrenceMessageEntity(BaseEntity, WithActiveMixin, TimestampMixin):
    event_occurrence_id: int
    parent_message_id: int | None = None
    event_id: int
    event_member_id: int | None = None

    text: str
    image: str | None = None
