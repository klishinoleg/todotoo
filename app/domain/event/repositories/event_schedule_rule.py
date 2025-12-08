from abc import ABC
from datetime import date

from core.enums.app.event.schedule_rule_type import ScheduleRuleType
from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository
from domain.event.entities.event_schedule_rule import EventScheduleRuleEntity


class EventScheduleRuleFilter[Q](BaseFilter[Q]):
    """
    Domain-level filter definition for EventScheduleRuleEntity.
    """

    type: EqualFilterField[ScheduleRuleType, Q] | None = None
    """Filter rules by schedule type (weekly, monthly, date)."""

    date: EqualFilterField[date, Q] | None = None
    """Filter rules bound to a specific calendar date."""

    day_of_week: EqualFilterField[int, Q] | None = None
    """Filter weekly rules by day of week (1–7)."""

    day_of_month: EqualFilterField[int, Q] | None = None
    """Filter monthly rules by day of month (1–31)."""

    start_time: RangeFilterField[int, Q] | None = None
    """Filter by start time (HHMM) using range or exact value."""

    end_time: RangeFilterField[int, Q] | None = None
    """Filter by end time (HHMM) using range or exact value."""


class EventScheduleRuleRepository[Q](BaseRepository[EventScheduleRuleEntity, EventScheduleRuleFilter[Q]], ABC):
    """
    Abstract repository for EventScheduleRuleEntity.
    """
    ...
