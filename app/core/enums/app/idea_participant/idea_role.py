from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class IdeaRoleEnum(BaseLabeledEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"
    CORE_MEMBER = "core_member"
    CONTRIBUTOR = "contributor"
    VIEWER = "viewer"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.OWNER: _("Owner"),
            cls.ADMIN: _("Admin"),
            cls.MODERATOR: _("Moderator"),
            cls.CORE_MEMBER: _("Core member"),
            cls.CONTRIBUTOR: _("Contributor"),
            cls.VIEWER: _("Viewer"),
        }

