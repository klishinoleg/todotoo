from dataclasses import dataclass

from core.di.auth import DIAuthProviderData
from core.enums.app.account.auth_provider import AuthProviderType
from infrastructure.auth.providers.oauth.base_oauth_data import OAuthProviderData


@dataclass(slots=True)
class AppleProviderData(OAuthProviderData):
    def __init__(self, provider_raw_data: dict) -> None:
        normalized = dict(provider_raw_data)
        normalized.setdefault("provider_user_id", provider_raw_data.get("sub"))

        # Apple may return first/last name only on the first login.
        user_block = provider_raw_data.get("user")
        if isinstance(user_block, dict):
            name_block = user_block.get("name")
            if isinstance(name_block, dict):
                normalized.setdefault("first_name", name_block.get("firstName"))
                normalized.setdefault("last_name", name_block.get("lastName"))
            normalized.setdefault("email", user_block.get("email"))

        super().__init__(normalized)


DIAuthProviderData.register(AuthProviderType.APPLE, AppleProviderData)

