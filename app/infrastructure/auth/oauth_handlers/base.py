from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from typing import Any, cast

from core.enums.system.error_fields import ErrorFields
from core.enums.system.logger.message_levels import LogMessageLevel
from core.logger.logger import Logger
from domain.base.exceptions import DomainValidationException


class OAuthProviderHandler(ABC):
    @abstractmethod
    def build_authorize_url(self, state: str, redirect_uri: str | None = None) -> str:
        ...

    @abstractmethod
    def exchange_code(
            self,
            code: str,
            redirect_uri: str | None = None,
            user: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        ...


class OAuthHandlerSupport:
    @staticmethod
    def require_config(value: str, name: str) -> str:
        val = str(value or "").strip()
        if not val:
            raise DomainValidationException(
                f"OAuth provider is not configured: {name}",
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        return val

    @staticmethod
    def http_get_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
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
    def http_post_form_json(url: str, data: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
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
    def decode_jwt_payload(token: str) -> dict[str, Any]:
        parts = token.split(".")
        if len(parts) < 2:
            return {}
        try:
            payload_raw = OAuthHandlerSupport.from_b64url(parts[1])
            payload = json.loads(payload_raw.decode("utf-8"))
            if isinstance(payload, dict):
                return payload
        except Exception:
            return {}
        return {}

    @staticmethod
    def attach_raw_data(payload: dict[str, Any]) -> dict[str, Any]:
        raw_data = payload.get("raw_data")
        if isinstance(raw_data, dict):
            payload["raw_data"] = dict(raw_data)
            return payload

        payload["raw_data"] = {key: value for key, value in payload.items() if key != "raw_data"}
        return payload

    @staticmethod
    def from_b64url(data: str) -> bytes:
        padding = "=" * ((4 - len(data) % 4) % 4)
        return base64.urlsafe_b64decode(data + padding)
