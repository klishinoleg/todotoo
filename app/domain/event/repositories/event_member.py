from abc import ABC
from datetime import datetime

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository
from domain.event.entities.event_member import EventMemberEntity


class EventMemberFilter[Q](BaseFilter[Q]):
    """
    Domain-level filter definition for EventMemberEntity.

    Concrete repositories must translate these filters into ORM queries by
    delegating to each field's `extend_query` implementation.
    """

    event_id: EqualFilterField[int, Q] | None = None
    """Filter members by related event ID."""

    event_occurrence_id: EqualFilterField[int, Q] | None = None
    """Filter members by specific event occurrence ID."""

    account_id: EqualFilterField[int, Q] | None = None
    """Filter members by related account/user ID."""

    has_accepted: BoolFilterField[Q] | None = None
    """Filter by participation status (accepted / not accepted)."""

    created_at: RangeFilterField[datetime, Q] | None = None
    """Filter by creation time: from_value ≤ created_at ≤ to_value."""

    is_active: BoolFilterField[Q] | None = None
    """Filter members by active/inactive state (if supported by entity)."""


class EventMemberRepository[Q](
    BaseRepository[EventMemberEntity, EventMemberFilter[Q]], ABC
):
    """
    Abstract repository for EventMemberEntity.

    Responsibilities:
        - Provide CRUD operations for event members (see BaseRepository).
        - Implement filtered_list() using EventMemberFilter and its field filters.
        - Encapsulate persistence details (ORM, DB) from the domain layer.
    """
    ...
