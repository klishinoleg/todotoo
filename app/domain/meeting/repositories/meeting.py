from abc import ABC
from datetime import datetime

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.filters.string_filters import TextFilterField
from domain.base.repository import BaseRepository
from domain.meeting.entities.meeting import MeetingEntity
from domain.meeting.entities.meeting_participant import MeetingParticipantEntity


class MeetingFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    type: EqualFilterField[str, Q] | None = None
    title: TextFilterField[Q] | None = None
    start_datetime: RangeFilterField[datetime, Q] | None = None
    end_datetime: RangeFilterField[datetime, Q] | None = None


class MeetingRepository[Q](BaseRepository[MeetingEntity, MeetingFilter[Q]], ABC):
    ...


class MeetingParticipantFilter[Q](BaseFilter[Q]):
    meeting_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    status: EqualFilterField[str, Q] | None = None


class MeetingParticipantRepository[Q](BaseRepository[MeetingParticipantEntity, MeetingParticipantFilter[Q]], ABC):
    ...
