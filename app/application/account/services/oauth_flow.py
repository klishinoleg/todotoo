from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, cast

from jose import jwt
from jose.constants import ALGORITHMS

from application.account.dto.auth.oauth_flow import OAuthAuthorizeUrlDTO
from core.config.settings import settings
from core.enums.app.account.auth_provider import AuthActionType, AuthProviderType
from core.enums.system.error_fields import ErrorFields
from core.enums.system.logger.message_levels import LogMessageLevel
from core.logger.logger import Logger
from domain.base.exceptions import DomainValidationException

_STATE_TTL_SECONDS = 10 * 60


class OAuthFlowService:
    _supported_providers = {
        AuthProviderType.GOOGLE,
        AuthProviderType.APPLE,
        AuthProviderType.FACEBOOK,
    }

    def ensure_supported_provider(self, provider_type: AuthProviderType) -> None:
        if provider_type not in self._supported_providers:
            raise DomainValidationException(
                f"OAuth flow is not supported for provider: {provider_type}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

    def build_authorize_url(
            self,
            provider_type: AuthProviderType,
            action_type: AuthActionType,
            redirect_uri: str | None = None,
    ) -> OAuthAuthorizeUrlDTO:
        self.ensure_supported_provider(provider_type)
        state = self._create_signed_state(provider_type, action_type)

        if provider_type == AuthProviderType.GOOGLE:
            auth_url = self._build_google_auth_url(state, redirect_uri)
        elif provider_type == AuthProviderType.FACEBOOK:
            auth_url = self._build_facebook_auth_url(state, redirect_uri)
        elif provider_type == AuthProviderType.APPLE:
            auth_url = self._build_apple_auth_url(state, redirect_uri)
        else:
            raise DomainValidationException(
                f"OAuth flow is not supported for provider: {provider_type}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        return OAuthAuthorizeUrlDTO(
            provider_type=provider_type,
            action_type=action_type,
            auth_url=auth_url,
            state=state,
        )

    async def exchange_code_for_provider_data(
            self,
            provider_type: AuthProviderType,
            code: str,
            redirect_uri: str | None = None,
            user: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.ensure_supported_provider(provider_type)
        Logger.auth(
            "oauth.exchange.start",
            provider_type=str(provider_type),
            has_code=bool(code),
            redirect_uri=redirect_uri,
            has_user=bool(user),
        )
        return await asyncio.to_thread(
            self._exchange_code_for_provider_data_sync,
            provider_type,
            code,
            redirect_uri,
            user,
        )

    def resolve_action_type(
            self,
            provider_type: AuthProviderType,
            state: str | None,
            fallback_action: AuthActionType | None,
    ) -> AuthActionType:
        if state:
            payload = self._verify_signed_state(state)
            if payload.get("provider_type") != str(provider_type):
                raise DomainValidationException(
                    "OAuth state provider mismatch",
                    field=ErrorFields.AUTH_PROVIDER_DATA,
                )
            try:
                return AuthActionType(payload["action_type"])
            except Exception:
                raise DomainValidationException(
                    "OAuth state action is invalid",
                    field=ErrorFields.AUTH_PROVIDER_DATA,
                )

        if fallback_action:
            return fallback_action

        return AuthActionType.LOGIN

    def _exchange_code_for_provider_data_sync(
            self,
            provider_type: AuthProviderType,
            code: str,
            redirect_uri: str | None = None,
            user: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if provider_type == AuthProviderType.GOOGLE:
            return self._google_exchange(code, redirect_uri)
        if provider_type == AuthProviderType.FACEBOOK:
            return self._facebook_exchange(code, redirect_uri)
        if provider_type == AuthProviderType.APPLE:
            return self._apple_exchange(code, redirect_uri, user)
        raise DomainValidationException(
            f"OAuth flow is not supported for provider: {provider_type}",
            field=ErrorFields.AUTH_PROVIDER_DATA,
        )

    @staticmethod
    def _to_b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode().rstrip("=")

    @staticmethod
    def _from_b64url(data: str) -> bytes:
        padding = "=" * ((4 - len(data) % 4) % 4)
        return base64.urlsafe_b64decode(data + padding)

    def _create_signed_state(self, provider_type: AuthProviderType, action_type: AuthActionType) -> str:
        payload = {
            "provider_type": str(provider_type),
            "action_type": str(action_type),
            "ts": int(time.time()),
            "nonce": secrets.token_urlsafe(16),
        }
        payload_raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode()
        payload_b64 = self._to_b64url(payload_raw)
        signature = hmac.new(
            settings.auth.access_token_secret_key.encode(),
            payload_b64.encode(),
            hashlib.sha256,
        ).hexdigest()
        return f"{payload_b64}.{signature}"

    def _verify_signed_state(self, state: str) -> dict[str, Any]:
        try:
            payload_b64, signature = state.split(".", 1)
        except ValueError:
            raise DomainValidationException("OAuth state is invalid", field=ErrorFields.AUTH_PROVIDER_DATA)

        expected_sig = hmac.new(
            settings.auth.access_token_secret_key.encode(),
            payload_b64.encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            raise DomainValidationException("OAuth state signature is invalid", field=ErrorFields.AUTH_PROVIDER_DATA)

        try:
            payload_raw = self._from_b64url(payload_b64)
            payload = json.loads(payload_raw.decode())
        except Exception:
            raise DomainValidationException("OAuth state payload is invalid", field=ErrorFields.AUTH_PROVIDER_DATA)

        ts = payload.get("ts")
        if not isinstance(ts, int):
            raise DomainValidationException("OAuth state timestamp is invalid", field=ErrorFields.AUTH_PROVIDER_DATA)
        if ts + _STATE_TTL_SECONDS < int(time.time()):
            raise DomainValidationException("OAuth state expired", field=ErrorFields.AUTH_PROVIDER_DATA)

        return cast(dict[str, Any], payload)

    @staticmethod
    def _require_config(value: str, name: str) -> str:
        val = str(value or "").strip()
        if not val:
            raise DomainValidationException(
                f"OAuth provider is not configured: {name}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        return val

    @staticmethod
    def _http_get_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
        req = urllib.request.Request(url, headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                payload = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            Logger.auth(
                "oauth.http.get.error",
                level=LogMessageLevel.WARN,
                code=exc.code,
                reason=str(exc.reason),
                body=body[:500],
                url=url,
            )
            raise DomainValidationException(
                f"OAuth provider HTTP error {exc.code}: {body or exc.reason}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        except urllib.error.URLError as exc:
            Logger.auth(
                "oauth.http.get.network_error",
                level=LogMessageLevel.WARN,
                reason=str(exc.reason),
                url=url,
            )
            raise DomainValidationException(
                f"OAuth provider network error: {exc.reason}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise DomainValidationException("OAuth provider returned invalid JSON", field=ErrorFields.AUTH_PROVIDER_DATA)
        return cast(dict[str, Any], data)

    @staticmethod
    def _http_post_form_json(url: str, data: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
        encoded = urllib.parse.urlencode(data).encode()
        final_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if headers:
            final_headers.update(headers)
        req = urllib.request.Request(url, data=encoded, headers=final_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                payload = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            Logger.auth(
                "oauth.http.post.error",
                level=LogMessageLevel.WARN,
                code=exc.code,
                reason=str(exc.reason),
                body=body[:500],
                url=url,
            )
            raise DomainValidationException(
                f"OAuth provider HTTP error {exc.code}: {body or exc.reason}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        except urllib.error.URLError as exc:
            Logger.auth(
                "oauth.http.post.network_error",
                level=LogMessageLevel.WARN,
                reason=str(exc.reason),
                url=url,
            )
            raise DomainValidationException(
                f"OAuth provider network error: {exc.reason}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        parsed = json.loads(payload)
        if not isinstance(parsed, dict):
            raise DomainValidationException("OAuth provider returned invalid JSON", field=ErrorFields.AUTH_PROVIDER_DATA)
        return cast(dict[str, Any], parsed)

    @staticmethod
    def _decode_jwt_payload(token: str) -> dict[str, Any]:
        parts = token.split(".")
        if len(parts) < 2:
            return {}
        try:
            payload_raw = OAuthFlowService._from_b64url(parts[1])
            payload = json.loads(payload_raw.decode("utf-8"))
            if isinstance(payload, dict):
                return payload
        except Exception:
            return {}
        return {}

    @staticmethod
    def _attach_raw_data(payload: dict[str, Any]) -> dict[str, Any]:
        # Ensure raw_data is JSON-serializable and not self-referential.
        raw_data = payload.get("raw_data")
        if isinstance(raw_data, dict):
            payload["raw_data"] = dict(raw_data)
            return payload

        payload["raw_data"] = {key: value for key, value in payload.items() if key != "raw_data"}
        return payload

    def _build_google_auth_url(self, state: str, redirect_uri: str | None = None) -> str:
        client_id = self._require_config(settings.auth.google_client_id, "AUTH_GOOGLE_CLIENT_ID")
        callback_uri = redirect_uri or self._require_config(
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

    def _google_exchange(self, code: str, redirect_uri: str | None = None) -> dict[str, Any]:
        client_id = self._require_config(settings.auth.google_client_id, "AUTH_GOOGLE_CLIENT_ID")
        client_secret = self._require_config(settings.auth.google_client_secret, "AUTH_GOOGLE_CLIENT_SECRET")
        callback_uri = redirect_uri or self._require_config(
            settings.auth.google_redirect_uri,
            "AUTH_GOOGLE_REDIRECT_URI",
        )

        token_response = self._http_post_form_json(
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
        id_token_claims = self._decode_jwt_payload(id_token) if id_token else {}
        userinfo: dict[str, Any] = {}
        if access_token:
            userinfo = self._http_get_json(
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

        userinfo = self._attach_raw_data(userinfo)
        Logger.auth(
            "oauth.google.userinfo.ready",
            provider_type=str(AuthProviderType.GOOGLE),
            has_sub=True,
            has_email=bool(userinfo.get("email")),
            has_email_verified=bool(userinfo.get("email_verified")),
        )
        return userinfo

    def _build_facebook_auth_url(self, state: str, redirect_uri: str | None = None) -> str:
        app_id = self._require_config(settings.auth.facebook_app_id, "AUTH_FACEBOOK_APP_ID")
        callback_uri = redirect_uri or self._require_config(
            settings.auth.facebook_redirect_uri,
            "AUTH_FACEBOOK_REDIRECT_URI",
        )
        query = urllib.parse.urlencode(
            {
                "client_id": app_id,
                "redirect_uri": callback_uri,
                "response_type": "code",
                "scope": "email,public_profile",
                "state": state,
            }
        )
        return f"https://www.facebook.com/v22.0/dialog/oauth?{query}"

    def _facebook_exchange(self, code: str, redirect_uri: str | None = None) -> dict[str, Any]:
        app_id = self._require_config(settings.auth.facebook_app_id, "AUTH_FACEBOOK_APP_ID")
        app_secret = self._require_config(settings.auth.facebook_app_secret, "AUTH_FACEBOOK_APP_SECRET")
        callback_uri = redirect_uri or self._require_config(
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
        token_url = f"https://graph.facebook.com/v22.0/oauth/access_token?{token_query}"
        token_response = self._http_get_json(token_url)
        access_token = str(token_response.get("access_token") or "")
        if not access_token:
            raise DomainValidationException("Facebook access token not found", field=ErrorFields.AUTH_PROVIDER_DATA)

        user_query = urllib.parse.urlencode(
            {"fields": "id,name,email,picture", "access_token": access_token}
        )
        userinfo = self._http_get_json(f"https://graph.facebook.com/v22.0/me?{user_query}")
        return self._attach_raw_data(userinfo)

    def _build_apple_auth_url(self, state: str, redirect_uri: str | None = None) -> str:
        client_id = self._require_config(settings.auth.apple_client_id, "AUTH_APPLE_CLIENT_ID")
        callback_uri = redirect_uri or self._require_config(
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

    def _build_apple_client_secret(self) -> str:
        team_id = self._require_config(settings.auth.apple_team_id, "AUTH_APPLE_TEAM_ID")
        client_id = self._require_config(settings.auth.apple_client_id, "AUTH_APPLE_CLIENT_ID")
        key_id = self._require_config(settings.auth.apple_key_id, "AUTH_APPLE_KEY_ID")
        private_key = self._require_config(settings.auth.apple_private_key, "AUTH_APPLE_PRIVATE_KEY")

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

    def _apple_exchange(
            self,
            code: str,
            redirect_uri: str | None = None,
            user: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        client_id = self._require_config(settings.auth.apple_client_id, "AUTH_APPLE_CLIENT_ID")
        callback_uri = redirect_uri or self._require_config(
            settings.auth.apple_redirect_uri,
            "AUTH_APPLE_REDIRECT_URI",
        )
        client_secret = self._build_apple_client_secret()

        token_response = self._http_post_form_json(
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

        claims = self._decode_jwt_payload(id_token)
        if user:
            claims["user"] = user
        return self._attach_raw_data(claims)
