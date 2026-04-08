from __future__ import annotations

import urllib.parse
from typing import Any

from core.config.settings import settings
from core.enums.app.account.auth_provider import AuthProviderType
from core.enums.system.error_fields import ErrorFields
from core.enums.system.logger.message_levels import LogMessageLevel
from core.logger.logger import Logger
from domain.base.exceptions import DomainValidationException
from infrastructure.auth.oauth_handlers.base import OAuthHandlerSupport, OAuthProviderHandler


class GoogleOAuthHandler(OAuthProviderHandler):
    def build_authorize_url(self, state: str, redirect_uri: str | None = None) -> str:
        client_id = OAuthHandlerSupport.require_config(settings.auth.google_client_id, "AUTH_GOOGLE_CLIENT_ID")
        callback_uri = redirect_uri or OAuthHandlerSupport.require_config(
            settings.auth.google_redirect_uri,
            "AUTH_GOOGLE_REDIRECT_URI",
        )
        query = urllib.parse.urlencode(
            {
                "client_id": client_id,
                "redirect_uri": callback_uri,
                "response_type": "code",
                "scope": "openid email profile",
                "state": state,
            }
        )
        return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"

    def exchange_code(
            self,
            code: str,
            redirect_uri: str | None = None,
            user: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        client_id = OAuthHandlerSupport.require_config(settings.auth.google_client_id, "AUTH_GOOGLE_CLIENT_ID")
        client_secret = OAuthHandlerSupport.require_config(
            settings.auth.google_client_secret,
            "AUTH_GOOGLE_CLIENT_SECRET",
        )
        callback_uri = redirect_uri or OAuthHandlerSupport.require_config(
            settings.auth.google_redirect_uri,
            "AUTH_GOOGLE_REDIRECT_URI",
        )

        token_response = OAuthHandlerSupport.http_post_form_json(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": callback_uri,
                "grant_type": "authorization_code",
            },
        )
        Logger.auth(
            "oauth.google.token.exchanged",
            provider_type=str(AuthProviderType.GOOGLE),
            has_access_token=bool(token_response.get("access_token")),
            has_id_token=bool(token_response.get("id_token")),
            redirect_uri=callback_uri,
        )

        access_token = str(token_response.get("access_token") or "")
        id_token = str(token_response.get("id_token") or "")
        id_token_claims = OAuthHandlerSupport.decode_jwt_payload(id_token) if id_token else {}
        userinfo: dict[str, Any] = {}
        if access_token:
            userinfo = OAuthHandlerSupport.http_get_json(
                "https://openidconnect.googleapis.com/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )

        if not userinfo:
            userinfo = id_token_claims
        elif id_token_claims:
            for key in ("sub", "email", "email_verified", "given_name", "family_name", "picture"):
                if key not in userinfo and key in id_token_claims:
                    userinfo[key] = id_token_claims[key]

        if not userinfo.get("sub"):
            Logger.auth(
                "oauth.google.invalid_userinfo",
                level=LogMessageLevel.WARN,
                provider_type=str(AuthProviderType.GOOGLE),
                has_sub=False,
                has_email=bool(userinfo.get("email")),
                keys=sorted(list(userinfo.keys())),
            )
            raise DomainValidationException(
                "Google user identifier (sub) not found in oauth response",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        userinfo = OAuthHandlerSupport.attach_raw_data(userinfo)
        Logger.auth(
            "oauth.google.userinfo.ready",
            provider_type=str(AuthProviderType.GOOGLE),
            has_sub=True,
            has_email=bool(userinfo.get("email")),
            has_email_verified=bool(userinfo.get("email_verified")),
        )
        return userinfo
