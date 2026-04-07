from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from domain.account.entities.auth.provider_data import BaseAuthProviderData


@dataclass(slots=True)
class OAuthProviderData(BaseAuthProviderData):
    provider_id_type = str

    provider_user_id: str
    email: str | None
    email_verified: bool
    username: str | None
    first_name: str | None
    last_name: str | None
    avatar_url: str | None
    raw_data: dict[str, Any]

    def __init__(self, provider_raw_data: dict) -> None:
        super().__init__(provider_raw_data)
        self.provider_user_id = str(self._get_provider_user_id(provider_raw_data))
        self.email = self._get_optional_str(provider_raw_data, "email")
        self.email_verified = bool(provider_raw_data.get("email_verified", False))
        self.username = self._get_optional_str(provider_raw_data, "username")
        self.first_name = self._get_optional_str(provider_raw_data, "first_name")
        self.last_name = self._get_optional_str(provider_raw_data, "last_name")
        self.avatar_url = self._get_optional_str(provider_raw_data, "avatar_url")
        raw_data = provider_raw_data.get("raw_data")
        self.raw_data = raw_data if isinstance(raw_data, dict) else provider_raw_data

    @staticmethod
    def _get_optional_str(data: dict, key: str) -> str | None:
        value = data.get(key)
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    def _get_provider_user_id(self, provider_raw_data: dict) -> str:
        value = provider_raw_data.get("provider_user_id")
        if value is None:
            return ""
        return str(value)

    def is_valid(self) -> bool:
        return bool(self.provider_user_id)

    def prepare_for_storage(self) -> Self:
        self._provider_raw_data = {
            "provider_user_id": self.provider_user_id,
            "email": self.email,
            "email_verified": self.email_verified,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar_url": self.avatar_url,
            "raw_data": self.raw_data,
        }
        return self

    def get_user_id(self) -> str | int:
        return self.provider_user_id

    def get_username(self) -> str:
        if self.username:
            return self.username
        if self.email:
            return self.email
        provider_id = self.provider_user_id.strip()
        if provider_id:
            return f"oauth:{provider_id}"
        return "oauth:user"

    def get_public_name(self) -> str | None:
        full_name = " ".join(part for part in (self.first_name, self.last_name) if part).strip()
        if full_name:
            return full_name
        return self.username

    def get_is_premium(self) -> bool:
        return False

    def get_language_code(self) -> str | None:
        language = self._provider_raw_data.get("language_code")
        if language is None:
            return None
        return str(language)

    async def get_image_url(self) -> str | None:
        return self.avatar_url

    def get_contact_url(self) -> str | None:
        return None
