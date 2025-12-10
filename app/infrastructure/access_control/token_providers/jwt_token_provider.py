from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from jose.constants import ALGORITHMS

from core.config.settings import settings
from core.di.access_control import DIAccessTokenProvider
from core.enums.di.access_control import AccessTokenType
from core.exceptions.system import AccessControlException
from core.messages.system.no_localized_messages import SystemMessages
from infrastructure.access_control.token_provider import TokenProvider


class JwtTokenProvider(TokenProvider):
    """JWT implementation of TokenProvider."""

    ALGORITHM = ALGORITHMS.HS256

    def __init__(self) -> None:
        self.secret_key = settings.system.access_token_secret_key

    def create_token(self, user_id: int, expire_minutes: int | None = None) -> str:
        if not expire_minutes:
            expire_minutes = settings.system.access_token_expire_minutes
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return str(jwt.encode(payload, self.secret_key, algorithm=self.ALGORITHM))

    def decode_token(self, token: str) -> int:
        """
        Decode JWT and return user_id.
        Raise domain-level exceptions on error (expired / invalid).
        """

        try:
            data = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.ALGORITHM],
            )
            return int(data.get("sub"))

        except ExpiredSignatureError:
            # JWT expired
            raise AccessControlException(
                message=SystemMessages.ACCESS_TOKEN_EXPIRED
            )

        except JWTError:
            # Wrong signature, malformed token, tampering, wrong key, etc.
            raise AccessControlException(
                message=SystemMessages.INVALID_ACCESS_TOKEN
            )

        except Exception:
            raise AccessControlException(
                message=SystemMessages.UNKNOWN_ACCESS_CONTROL_ERROR
            )


DIAccessTokenProvider.register(AccessTokenType.JWT, JwtTokenProvider)
