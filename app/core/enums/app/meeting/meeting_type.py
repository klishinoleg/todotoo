from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class MeetingTypeEnum(BaseLabeledEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    HYBRID = "hybrid"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.ONLINE: _("Online"),
            cls.OFFLINE: _("Offline"),
            cls.HYBRID: _("Hybrid"),
        }

