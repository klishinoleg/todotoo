from abc import ABC
from datetime import datetime

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository
from domain.calendar.entities.calendar_item import CalendarItemEntity


class CalendarItemFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    type: EqualFilterField[str, Q] | None = None
    ref_id: EqualFilterField[int, Q] | None = None
    start_datetime: RangeFilterField[datetime, Q] | None = None
    end_datetime: RangeFilterField[datetime, Q] | None = None


class CalendarItemRepository[Q](BaseRepository[CalendarItemEntity, CalendarItemFilter[Q]], ABC):
    ...
