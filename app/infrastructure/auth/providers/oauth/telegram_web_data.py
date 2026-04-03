import hashlib
import hmac
import time
from dataclasses import dataclass

from core.config.settings import settings
from core.di.auth import DIAuthProviderData
from core.enums.app.account.auth_provider import AuthProviderType
from infrastructure.auth.providers.oauth.base_oauth_data import OAuthProviderData


@dataclass(slots=True)
class TelegramWebProviderData(OAuthProviderData):
    auth_lifetime_seconds: int = 24 * 60 * 60

    def __init__(self, provider_raw_data: dict) -> None:
        normalized = dict(provider_raw_data)
        normalized.setdefault("provider_user_id", provider_raw_data.get("id"))
        normalized.setdefault("avatar_url", provider_raw_data.get("photo_url"))
        normalized.setdefault("first_name", provider_raw_data.get("first_name"))
        normalized.setdefault("last_name", provider_raw_data.get("last_name"))
        normalized.setdefault("username", provider_raw_data.get("username"))
        super().__init__(normalized)

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False

        source = dict(self._provider_raw_data)
        received_hash = source.pop("hash", None)
        if not received_hash:
            return False

        auth_date_raw = source.get("auth_date")
        if auth_date_raw is None:
            return False
        try:
            auth_ts = int(auth_date_raw)
        except (TypeError, ValueError):
            return False
        if auth_ts + self.auth_lifetime_seconds < int(time.time()):
            return False

        pairs: list[str] = []
        for key in sorted(source):
            value = source[key]
            if value is None:
                continue
            pairs.append(f"{key}={value}")
        data_check_string = "\n".join(pairs)

        secret = hashlib.sha256(settings.auth.tg_bot_token.encode()).digest()
        generated_hash = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(generated_hash, str(received_hash))


DIAuthProviderData.register(AuthProviderType.TELEGRAM_WEB, TelegramWebProviderData)
