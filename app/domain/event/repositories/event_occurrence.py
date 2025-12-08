from abc import ABC
from datetime import datetime

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository
from domain.event.entities.event_occurrence import EventOccurrenceEntity


class EventOccurrenceFilter[Q](BaseFilter[Q]):
    """
    Domain-level filter definition for EventOccurrenceEntity.

    Concrete repositories must translate these filters into ORM queries by
    delegating to each field's `extend_query` implementation.
    """

    event_id: EqualFilterField[int, Q] | None = None
    """Filter occurrences belonging to a specific event."""

    location_id: EqualFilterField[int, Q] | None = None
    """Filter by related LocationEntity ID (if occurrence is linked to a location)."""

    is_finished: BoolFilterField[Q] | None = None
    """Filter by completion status (finished / not finished)."""

    is_canceled: BoolFilterField[Q] | None = None
    """Filter by cancellation flag."""

    start_at: RangeFilterField[datetime, Q] | None = None
    """Filter by start time: from_value ≤ start_at ≤ to_value."""

    end_at: RangeFilterField[datetime, Q] | None = None
    """Filter by end time: from_value ≤ end_at ≤ to_value."""

    members_count: RangeFilterField[int, Q] | None = None
    """Filter by members count (range or exact value)."""


class EventOccurrenceRepository[Q](
    BaseRepository[EventOccurrenceEntity, EventOccurrenceFilter[Q]], ABC
):
    """
    Abstract repository for EventOccurrenceEntity.

    Responsibilities:
        - Provide CRUD operations for event occurrences (see BaseRepository).
        - Implement filtered_list() using EventOccurrenceFilter and its field filters.
        - Encapsulate persistence details (ORM, DB) from the domain layer.
    """
    ...
