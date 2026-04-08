import hashlib
import hmac
from dataclasses import dataclass
from typing import Self
from urllib.parse import unquote

from core.config.settings import settings
from core.di.auth import DIAuthProviderData
from core.enums.app.account.auth_provider import AuthProviderType
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from infrastructure.auth.providers.telegram.telegram_types import TelegramInitData, TgChat, TgUser


@dataclass(slots=True)
class TelegramProviderData(BaseAuthProviderData):
    """
    Domain-level structure for working with Telegram provider data.
    Converts validated raw dict into typed TelegramInitData.
    """

    _telegram_data: TelegramInitData
    _u: TgUser
    provider_id_type = int

    def __init__(self, provider_raw_data: dict) -> None:
        super().__init__(provider_raw_data)

        normalized = dict(self._provider_raw_data)
        user = normalized.get("user")
        if isinstance(user, dict):
            normalized["user"] = TgUser(**user)
        receiver = normalized.get("receiver")
        if isinstance(receiver, dict):
            normalized["receiver"] = TgUser(**receiver)
        chat = normalized.get("chat")
        if isinstance(chat, dict):
            normalized["chat"] = TgChat(**chat)

        # Convert raw dict → typed dataclass
        self._telegram_data = TelegramInitData(**normalized)

        # Quick access to user
        self._u = self._telegram_data.user

    # -------- unified BaseAuthProviderData interface --------

    def get_user_id(self) -> str | int:
        return self._u.id

    def get_username(self) -> str:
        return self._u.username or f"TG:{self._u.id}"

    def get_public_name(self) -> str | None:
        first = self._u.first_name
        last = self._u.last_name
        username = self._u.username
        return username or f"{first}:{last or 'TG'}"

    def get_is_premium(self) -> bool:
        return bool(self._u.is_premium)

    def get_language_code(self) -> str | None:
        return self._u.language_code

    async def get_image_url(self) -> str | None:
        return self._u.photo_url

    def get_contact_url(self) -> str | None:
        username = self._u.username
        if username:
            return f"https://t.me/{username}"
        return None

    def is_valid(self) -> bool:
        """Validate Telegram WebApp init data."""
        init_data = self._telegram_data.init_data
        vals = {k: unquote(v) for k, v in [s.split("=", 1) for s in init_data.split("&")]}
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(vals.items()) if k != "hash")

        secret_key = hmac.new("WebAppData".encode(), settings.auth.tg_bot_token.encode(), hashlib.sha256).digest()
        h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
        return h.hexdigest() == vals["hash"]

    def prepare_for_storage(self) -> Self:
        return self


DIAuthProviderData.register(AuthProviderType.TELEGRAM, TelegramProviderData)
