from dataclasses import dataclass

from core.enums.app.meeting.meeting_participant_status import MeetingParticipantStatusEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class MeetingParticipantEntity(BaseEntity, TimestampMixin):
    meeting_id: int
    account_id: int
    status: MeetingParticipantStatusEnum = MeetingParticipantStatusEnum.MAYBE

