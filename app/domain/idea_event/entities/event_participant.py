from dataclasses import dataclass

from core.enums.app.idea_event.event_participant_status import EventParticipantStatusEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class IdeaEventParticipantEntity(BaseEntity, TimestampMixin):
    event_id: int
    account_id: int
    status: EventParticipantStatusEnum = EventParticipantStatusEnum.JOINED

