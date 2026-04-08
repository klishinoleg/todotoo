from __future__ import annotations

import urllib.parse
from typing import Any

from core.config.settings import settings
from core.enums.system.error_fields import ErrorFields
from domain.base.exceptions import DomainValidationException
from infrastructure.auth.oauth_handlers.base import OAuthHandlerSupport, OAuthProviderHandler
from infrastructure.auth.oauth_handlers.constants import (
    FACEBOOK_AUTHORIZE_URL,
    FACEBOOK_SCOPE,
    FACEBOOK_TOKEN_URL,
    FACEBOOK_USERINFO_URL,
    FACEBOOK_USER_FIELDS,
)


class FacebookOAuthHandler(OAuthProviderHandler):
    def build_authorize_url(self, state: str, redirect_uri: str | None = None) -> str:
        app_id = OAuthHandlerSupport.require_config(settings.auth.facebook_app_id, "AUTH_FACEBOOK_APP_ID")
        callback_uri = redirect_uri or OAuthHandlerSupport.require_config(
            settings.auth.facebook_redirect_uri,
            "AUTH_FACEBOOK_REDIRECT_URI",
        )
        query = urllib.parse.urlencode(
            {
                "client_id": app_id,
                "redirect_uri": callback_uri,
                "response_type": "code",
                "scope": FACEBOOK_SCOPE,
                "state": state,
            }
        )
        return f"{FACEBOOK_AUTHORIZE_URL}?{query}"

    def exchange_code(
            self,
            code: str,
            redirect_uri: str | None = None,
            user: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        app_id = OAuthHandlerSupport.require_config(settings.auth.facebook_app_id, "AUTH_FACEBOOK_APP_ID")
        app_secret = OAuthHandlerSupport.require_config(settings.auth.facebook_app_secret, "AUTH_FACEBOOK_APP_SECRET")
        callback_uri = redirect_uri or OAuthHandlerSupport.require_config(
            settings.auth.facebook_redirect_uri,
            "AUTH_FACEBOOK_REDIRECT_URI",
        )

        token_query = urllib.parse.urlencode(
            {
                "client_id": app_id,
                "client_secret": app_secret,
                "redirect_uri": callback_uri,
                "code": code,
            }
        )
        token_url = f"{FACEBOOK_TOKEN_URL}?{token_query}"
        token_response = OAuthHandlerSupport.http_get_json(token_url)
        access_token = str(token_response.get("access_token") or "")
        if not access_token:
            raise DomainValidationException("Facebook access token not found", field=ErrorFields.AUTH_PROVIDER_DATA)

        user_query = urllib.parse.urlencode(
            {"fields": FACEBOOK_USER_FIELDS, "access_token": access_token}
        )
        userinfo = OAuthHandlerSupport.http_get_json(f"{FACEBOOK_USERINFO_URL}?{user_query}")
        return OAuthHandlerSupport.attach_raw_data(userinfo)
