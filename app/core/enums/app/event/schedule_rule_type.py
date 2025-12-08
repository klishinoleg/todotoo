from anyio.functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class ScheduleRuleType(BaseLabeledEnum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    DATE = "date"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.WEEKLY: _("Weekly"),
            cls.MONTHLY: _("Monthly"),
            cls.DATE: _("Day"),
        }
