from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any, cast

from application.account.dto.auth.oauth_flow import OAuthAuthorizeUrlDTO
from core.config.settings import settings
from core.enums.app.account.auth_provider import AuthActionType, AuthProviderType
from core.enums.system.error_fields import ErrorFields
from core.logger.logger import Logger
from domain.base.exceptions import DomainValidationException
from infrastructure.auth.oauth_handlers.base import OAuthHandlerSupport
from infrastructure.auth.oauth_handlers.registry import get_oauth_handler, get_supported_oauth_providers

_STATE_TTL_SECONDS = 10 * 60


class OAuthFlowService:
    def ensure_supported_provider(self, provider_type: AuthProviderType) -> None:
        if provider_type not in get_supported_oauth_providers():
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
        auth_url = get_oauth_handler(provider_type).build_authorize_url(state, redirect_uri)

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
        return get_oauth_handler(provider_type).exchange_code(code, redirect_uri, user)

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
    def _attach_raw_data(payload: dict[str, Any]) -> dict[str, Any]:
        return OAuthHandlerSupport.attach_raw_data(payload)
