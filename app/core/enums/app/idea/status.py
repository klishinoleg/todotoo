from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class IdeaStatusEnum(BaseLabeledEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.DRAFT: _("Draft"),
            cls.ACTIVE: _("Active"),
            cls.ON_HOLD: _("On hold"),
            cls.COMPLETED: _("Completed"),
            cls.ARCHIVED: _("Archived"),
        }

