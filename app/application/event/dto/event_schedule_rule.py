from datetime import date

from application.base.dto.base import ItemDTO, ListDTO
from core.enums.app.event.schedule_rule_type import ScheduleRuleType


class EventScheduleRuleDTO(ItemDTO):
    """
    Full representation of EventScheduleRuleEntity for external interfaces.
    Mirrors domain schedule rule fields suitable for UI and integrations.
    """
    type: ScheduleRuleType
    date: date | None
    day_of_week: int | None  # 1–7
    day_of_month: int | None  # 1–31
    start_time: int | None  # HHMM
    end_time: int | None  # HHMM


class EventScheduleRuleListDTO(ListDTO):
    """
    Lightweight version of EventScheduleRuleDTO for list views.
    Only fields required by listings are included.
    """
    type: ScheduleRuleType
    date: date | None
    day_of_week: int | None  # 1–7
    day_of_month: int | None  # 1–31
    start_time: int | None  # HHMM
    end_time: int | None  # HHMM
