from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class EventMemberEntity(BaseEntity, TimestampMixin):
    event_occurrence_id: int
    event_id: int
    account_id: int
    has_accepted: bool = False
