from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class MeetingParticipantStatusEnum(BaseLabeledEnum):
    GOING = "going"
    DECLINED = "declined"
    MAYBE = "maybe"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.GOING: _("Going"),
            cls.DECLINED: _("Declined"),
            cls.MAYBE: _("Maybe"),
        }

