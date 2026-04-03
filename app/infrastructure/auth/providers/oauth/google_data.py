from dataclasses import dataclass

from core.di.auth import DIAuthProviderData
from core.enums.app.account.auth_provider import AuthProviderType
from infrastructure.auth.providers.oauth.base_oauth_data import OAuthProviderData


@dataclass(slots=True)
class GoogleProviderData(OAuthProviderData):
    def __init__(self, provider_raw_data: dict) -> None:
        normalized = dict(provider_raw_data)
        normalized.setdefault("provider_user_id", provider_raw_data.get("sub"))
        normalized.setdefault("first_name", provider_raw_data.get("given_name"))
        normalized.setdefault("last_name", provider_raw_data.get("family_name"))
        normalized.setdefault("avatar_url", provider_raw_data.get("picture"))
        super().__init__(normalized)


DIAuthProviderData.register(AuthProviderType.GOOGLE, GoogleProviderData)

