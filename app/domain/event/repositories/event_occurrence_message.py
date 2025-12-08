from abc import ABC
from datetime import datetime

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.filters.string_filters import StringContainsFilterField
from domain.base.repository import BaseRepository
from domain.event.entities.event_occurrence_message import EventOccurrenceMessageEntity


class EventOccurrenceMessageFilter[Q](BaseFilter[Q]):
    """
    Domain-level filter definition for EventOccurrenceMessageEntity.

    Concrete repositories must translate these filters into ORM queries by
    delegating to each field's `extend_query` implementation.
    """

    event_id: EqualFilterField[int, Q] | None = None
    """Filter messages by parent event ID."""

    event_occurrence_id: EqualFilterField[int, Q] | None = None
    """Filter messages by specific event occurrence."""

    parent_message_id: EqualFilterField[int, Q] | None = None
    """Filter replies by parent message ID (None for root messages)."""

    event_member_id: EqualFilterField[int, Q] | None = None
    """Filter messages authored by a specific event member."""

    text: StringContainsFilterField[Q] | None = None
    """Substring search over message text."""

    created_at: RangeFilterField[datetime, Q] | None = None
    """Filter by creation time: from_value ≤ created_at ≤ to_value."""

    is_active: BoolFilterField[Q] | None = None
    """Filter messages by active/inactive state."""


class EventOccurrenceMessageRepository[Q](
    BaseRepository[EventOccurrenceMessageEntity, EventOccurrenceMessageFilter[Q]], ABC
):
    """
    Abstract repository for EventOccurrenceMessageEntity.

    Responsibilities:
        - Provide CRUD operations for messages (see BaseRepository).
        - Implement filtered_list() using EventOccurrenceMessageFilter.
        - Hide persistence / ORM details from the domain layer.
    """
    ...
