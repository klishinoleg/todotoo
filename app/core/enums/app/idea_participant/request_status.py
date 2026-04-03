from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class RequestStatusEnum(BaseLabeledEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.PENDING: _("Pending"),
            cls.APPROVED: _("Approved"),
            cls.REJECTED: _("Rejected"),
        }

