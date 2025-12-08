from datetime import date

from tortoise import fields

from core.enums.app.event.schedule_rule_type import ScheduleRuleType
from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class EventScheduleRuleModel(BaseTortoiseModel):
    """
    Tortoise ORM model for EventScheduleRuleEntity.

    Describes recurring / one-time schedule rules for events.
    """

    type: ScheduleRuleType = fields.CharEnumField(
        ScheduleRuleType,
        description="Schedule type (weekly, monthly, date).",
    )

    # For DATE type
    date: date | None = fields.DateField(
        null=True,
        description="Exact calendar date for 'date' type rules.",
    )

    # For WEEKLY type: 1–7 (e.g. Monday=1)
    day_of_week: int | None = fields.IntField(
        null=True,
        description="Day of week (1–7) for weekly rules.",
    )

    # For MONTHLY type: 1–31
    day_of_month: int | None = fields.IntField(
        null=True,
        description="Day of month (1–31) for monthly rules.",
    )

    # HHMM integer, e.g. 930 → 09:30
    start_time: int | None = fields.IntField(
        null=True,
        description="Start time in HHMM format.",
    )
    end_time: int | None = fields.IntField(
        null=True,
        description="End time in HHMM format.",
    )

    class Meta:
        table = "event_schedule_rules"
        description = "Event schedule rules (weekly/monthly/one-time)"
