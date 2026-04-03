from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class ParticipantStatusEnum(BaseLabeledEnum):
    ACTIVE = "active"
    PENDING = "pending"
    DECLINED = "declined"
    BLOCKED = "blocked"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.ACTIVE: _("Active"),
            cls.PENDING: _("Pending"),
            cls.DECLINED: _("Declined"),
            cls.BLOCKED: _("Blocked"),
        }

