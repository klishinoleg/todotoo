from __future__ import annotations

from core.enums.app.account.auth_provider import AuthProviderType
from core.enums.system.error_fields import ErrorFields
from domain.base.exceptions import DomainValidationException
from infrastructure.auth.oauth_handlers.apple import AppleOAuthHandler
from infrastructure.auth.oauth_handlers.base import OAuthProviderHandler
from infrastructure.auth.oauth_handlers.facebook import FacebookOAuthHandler
from infrastructure.auth.oauth_handlers.google import GoogleOAuthHandler

_HANDLERS: dict[AuthProviderType, OAuthProviderHandler] = {
    AuthProviderType.GOOGLE: GoogleOAuthHandler(),
    AuthProviderType.FACEBOOK: FacebookOAuthHandler(),
    AuthProviderType.APPLE: AppleOAuthHandler(),
}


def get_oauth_handler(provider_type: AuthProviderType) -> OAuthProviderHandler:
    handler = _HANDLERS.get(provider_type)
    if handler is None:
        raise DomainValidationException(
            f"OAuth flow is not supported for provider: {provider_type}",
            field=ErrorFields.AUTH_PROVIDER_DATA,
        )
    return handler


def get_supported_oauth_providers() -> set[AuthProviderType]:
    return set(_HANDLERS.keys())
