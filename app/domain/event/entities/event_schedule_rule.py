from dataclasses import dataclass
from datetime import date

from core.enums.app.event.schedule_rule_type import ScheduleRuleType
from domain.base.entity import BaseEntity


@dataclass(slots=True, kw_only=True)
class EventScheduleRuleEntity(BaseEntity):
    type: ScheduleRuleType
    date: date | None = None
    day_of_week: int | None = None  # 1–7
    day_of_month: int | None = None  # 1–31
    start_time: int | None = None  # HHMM
    end_time: int | None = None
