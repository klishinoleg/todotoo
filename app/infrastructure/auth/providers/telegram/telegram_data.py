from dataclasses import dataclass

from core.di.auth import DIAuthProviderData
from core.enums.app.account.auth_provider import AuthProviderType
from domain.account.entities.auth.provider_data import BaseProviderData
from infrastructure.auth.providers.telegram.telegram_types import TelegramInitData, TgUser


@dataclass(slots=True)
class TelegramProviderData(BaseProviderData):
    """
    Domain-level structure for working with Telegram provider data.
    Converts validated raw dict into typed TelegramInitData.
    """

    _telegram_data: TelegramInitData
    _u: TgUser

    def __init__(self, provider_raw_data: dict) -> None:
        super().__init__(provider_raw_data)

        # Convert raw dict → typed dataclass
        self._telegram_data = TelegramInitData(**self._provider_raw_data)

        # Quick access to user
        self._u = self._telegram_data.user

    # -------- unified BaseProviderData interface --------

    def get_user_id(self) -> str | int:
        return self._u.id

    def get_username(self) -> str | None:
        return self._u.username

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


DIAuthProviderData.register(AuthProviderType.TELEGRAM, TelegramProviderData)
