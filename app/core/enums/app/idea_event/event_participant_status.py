from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class EventParticipantStatusEnum(BaseLabeledEnum):
    JOINED = "joined"
    LEFT = "left"
    REMOVED = "removed"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.JOINED: _("Joined"),
            cls.LEFT: _("Left"),
            cls.REMOVED: _("Removed"),
        }

