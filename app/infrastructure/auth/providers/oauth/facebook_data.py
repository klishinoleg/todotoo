from dataclasses import dataclass
from typing import Any

from core.di.auth import DIAuthProviderData
from core.enums.app.account.auth_provider import AuthProviderType
from infrastructure.auth.providers.oauth.base_oauth_data import OAuthProviderData


@dataclass(slots=True)
class FacebookProviderData(OAuthProviderData):
    def __init__(self, provider_raw_data: dict) -> None:
        normalized = dict(provider_raw_data)
        normalized.setdefault("provider_user_id", provider_raw_data.get("id"))

        name = provider_raw_data.get("name")
        if isinstance(name, str) and name and " " in name:
            first, _, last = name.partition(" ")
            normalized.setdefault("first_name", first)
            normalized.setdefault("last_name", last)
            normalized.setdefault("username", name)
        elif isinstance(name, str):
            normalized.setdefault("username", name)

        picture = provider_raw_data.get("picture")
        if isinstance(picture, dict):
            data: Any = picture.get("data")
            if isinstance(data, dict):
                normalized.setdefault("avatar_url", data.get("url"))

        super().__init__(normalized)


DIAuthProviderData.register(AuthProviderType.FACEBOOK, FacebookProviderData)

