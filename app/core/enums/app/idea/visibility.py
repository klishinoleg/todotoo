from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class IdeaVisibilityEnum(BaseLabeledEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    INVITE_ONLY = "invite_only"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.PUBLIC: _("Public"),
            cls.PRIVATE: _("Private"),
            cls.INVITE_ONLY: _("Invite only"),
        }

