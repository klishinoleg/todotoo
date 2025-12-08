from abc import ABC

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.geometry_filter import GeometryFilterField
from domain.base.filters.string_filters import StringContainsFilterField
from domain.base.repository import BaseRepository
from domain.event.entities.event import EventEntity


class EventFilter[Q](BaseFilter[Q]):
    """
    Domain-level filter definition for EventEntity.

    Fields correspond to high-level query parameters.
    Concrete repositories must translate these into ORM queries by delegating
    to each field's `extend_query` method.
    """
    account_id: EqualFilterField[int, Q] | None = None
    name: StringContainsFilterField[Q] | None = None
    description: StringContainsFilterField[Q] | None = None
    is_active: BoolFilterField[Q] | None = None
    point: GeometryFilterField[Q] | None = None
    polygon: GeometryFilterField[Q] | None = None
    location_id: EqualFilterField[int, Q] | None = None
    schedule_rules: EqualFilterField[int, Q] | None = None
    """
    Filter by schedule rule IDs.

    Typical usage: find events that reference a particular schedule rule.
    Concrete repository may decide whether this is "has any of" or "contains all".
    """


class EventRepository[Q](BaseRepository[EventEntity, EventFilter[Q]], ABC):
    """
    Abstract repository for EventEntity.

    Responsibilities:
        - Provide CRUD operations for events (see BaseRepository).
        - Implement filtered_list() using EventFilter and its field filters.
        - Hide persistence/ORM details from the domain layer.
    """
    ...
