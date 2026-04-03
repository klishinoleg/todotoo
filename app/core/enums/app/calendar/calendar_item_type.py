from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class CalendarItemTypeEnum(BaseLabeledEnum):
    MEETING = "meeting"
    EVENT = "event"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.MEETING: _("Meeting"),
            cls.EVENT: _("Event"),
        }

