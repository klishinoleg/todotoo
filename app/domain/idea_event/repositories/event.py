from abc import ABC
from datetime import datetime

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.filters.string_filters import TextFilterField
from domain.base.repository import BaseRepository
from domain.idea_event.entities.event_comment import IdeaEventCommentEntity
from domain.idea_event.entities.event_media import IdeaEventMediaEntity
from domain.idea_event.entities.event_participant import IdeaEventParticipantEntity
from domain.idea_event.entities.event_reaction import IdeaEventReactionEntity
from domain.idea_event.entities.idea_event import IdeaEventEntity


class IdeaEventFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    created_by: EqualFilterField[int, Q] | None = None
    is_free_join: EqualFilterField[bool, Q] | None = None
    title: TextFilterField[Q] | None = None
    start_datetime: RangeFilterField[datetime, Q] | None = None
    end_datetime: RangeFilterField[datetime, Q] | None = None


class IdeaEventRepository[Q](BaseRepository[IdeaEventEntity, IdeaEventFilter[Q]], ABC):
    ...


class IdeaEventParticipantFilter[Q](BaseFilter[Q]):
    event_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    status: EqualFilterField[str, Q] | None = None


class IdeaEventParticipantRepository[Q](BaseRepository[IdeaEventParticipantEntity, IdeaEventParticipantFilter[Q]], ABC):
    ...


class IdeaEventMediaFilter[Q](BaseFilter[Q]):
    event_id: EqualFilterField[int, Q] | None = None
    created_by: EqualFilterField[int, Q] | None = None
    type: EqualFilterField[str, Q] | None = None


class IdeaEventMediaRepository[Q](BaseRepository[IdeaEventMediaEntity, IdeaEventMediaFilter[Q]], ABC):
    ...


class IdeaEventCommentFilter[Q](BaseFilter[Q]):
    event_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    text: TextFilterField[Q] | None = None


class IdeaEventCommentRepository[Q](BaseRepository[IdeaEventCommentEntity, IdeaEventCommentFilter[Q]], ABC):
    ...


class IdeaEventReactionFilter[Q](BaseFilter[Q]):
    event_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None


class IdeaEventReactionRepository[Q](BaseRepository[IdeaEventReactionEntity, IdeaEventReactionFilter[Q]], ABC):
    ...
