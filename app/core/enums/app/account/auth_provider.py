from functools import lru_cache
from typing import Dict

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class AuthProviderType(BaseLabeledEnum):
    TELEGRAM = "telegram"
    TELEGRAM_WEB = "telegram_web"
    PASSWORD = "password"
    GOOGLE = "google"
    APPLE = "apple"
    FACEBOOK = "facebook"
    FAKE = "fake"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> Dict[str, str]:
        return {
            cls.TELEGRAM: _("Telegram auth"),
            cls.TELEGRAM_WEB: _("Telegram Web auth"),
            cls.PASSWORD: _("Password auth"),
            cls.GOOGLE: _("Google auth"),
            cls.APPLE: _("Apple auth"),
            cls.FACEBOOK: _("Facebook auth"),
            cls.FAKE: _("Fake auth"),
        }


class AuthActionType(BaseLabeledEnum):
    LOGIN = "login"
    REGISTER = "register"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> Dict[str, str]:
        return {
            cls.LOGIN: _("Login"),
            cls.REGISTER: _("Register"),
        }
