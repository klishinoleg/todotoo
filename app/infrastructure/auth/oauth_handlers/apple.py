from __future__ import annotations

import time
import urllib.parse
from typing import Any

from jose import jwt
from jose.constants import ALGORITHMS

from core.config.settings import settings
from core.enums.system.error_fields import ErrorFields
from domain.base.exceptions import DomainValidationException
from infrastructure.auth.oauth_handlers.base import OAuthHandlerSupport, OAuthProviderHandler


class AppleOAuthHandler(OAuthProviderHandler):
    def build_authorize_url(self, state: str, redirect_uri: str | None = None) -> str:
        client_id = OAuthHandlerSupport.require_config(settings.auth.apple_client_id, "AUTH_APPLE_CLIENT_ID")
        callback_uri = redirect_uri or OAuthHandlerSupport.require_config(
            settings.auth.apple_redirect_uri,
            "AUTH_APPLE_REDIRECT_URI",
        )
        query = urllib.parse.urlencode(
            {
                "response_type": "code",
                "response_mode": "form_post",
                "client_id": client_id,
                "redirect_uri": callback_uri,
                "scope": "name email",
                "state": state,
            }
        )
        return f"https://appleid.apple.com/auth/authorize?{query}"

    def exchange_code(
            self,
            code: str,
            redirect_uri: str | None = None,
            user: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        client_id = OAuthHandlerSupport.require_config(settings.auth.apple_client_id, "AUTH_APPLE_CLIENT_ID")
        callback_uri = redirect_uri or OAuthHandlerSupport.require_config(
            settings.auth.apple_redirect_uri,
            "AUTH_APPLE_REDIRECT_URI",
        )
        client_secret = self._build_apple_client_secret()

        token_response = OAuthHandlerSupport.http_post_form_json(
            "https://appleid.apple.com/auth/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": callback_uri,
            },
        )
        id_token = str(token_response.get("id_token") or "")
        if not id_token:
            raise DomainValidationException("Apple id_token not found", field=ErrorFields.AUTH_PROVIDER_DATA)

        claims = OAuthHandlerSupport.decode_jwt_payload(id_token)
        if user:
            claims["user"] = user
        return OAuthHandlerSupport.attach_raw_data(claims)

    @staticmethod
    def _build_apple_client_secret() -> str:
        team_id = OAuthHandlerSupport.require_config(settings.auth.apple_team_id, "AUTH_APPLE_TEAM_ID")
        client_id = OAuthHandlerSupport.require_config(settings.auth.apple_client_id, "AUTH_APPLE_CLIENT_ID")
        key_id = OAuthHandlerSupport.require_config(settings.auth.apple_key_id, "AUTH_APPLE_KEY_ID")
        private_key = OAuthHandlerSupport.require_config(settings.auth.apple_private_key, "AUTH_APPLE_PRIVATE_KEY")

        now_ts = int(time.time())
        payload = {
            "iss": team_id,
            "iat": now_ts,
            "exp": now_ts + 300,
            "aud": "https://appleid.apple.com",
            "sub": client_id,
        }
        return str(
            jwt.encode(
                payload,
                private_key,
                algorithm=ALGORITHMS.ES256,
                headers={"kid": key_id},
            )
        )
