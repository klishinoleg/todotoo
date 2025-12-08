from functools import lru_cache
from typing import Dict

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class AuthProviderType(BaseLabeledEnum):
    TELEGRAM = "telegram"
    PASSWORD = "password"
    FAKE = "fake"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> Dict[str, str]:
        return {
            cls.TELEGRAM: _("Telegram auth"),
            cls.PASSWORD: _("Password auth"),
            cls.FAKE: _("Fake auth"),
        }
