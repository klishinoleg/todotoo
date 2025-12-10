from core.enums.di.access_control import AccessTokenType, PasswordHasherType
from core.exceptions.system import AccessControlException
from core.messages.system.no_localized_messages import SystemMessages
from infrastructure.access_control.password_hasher import PasswordHasher
from infrastructure.access_control.token_provider import TokenProvider
from core.config.settings import settings


class DIAccessTokenProvider:
    _providers: dict[AccessTokenType, type[TokenProvider]] = {}

    @classmethod
    def get(cls, token_type: AccessTokenType | None = None) -> TokenProvider:
        if not token_type:
            token_type = settings.system.default_access_token_type
        token_provider = cls._providers.get(token_type)
        if not token_provider:
            raise AccessControlException(SystemMessages.ACCESS_CONTROL_PROVIDER_NOT_REGISTERED)
        return token_provider()

    @classmethod
    def register(cls, token_type: AccessTokenType, provider: type[TokenProvider]) -> None:
        cls._providers[token_type] = provider


class DIPasswordHasherProvider:
    _hashers: dict[PasswordHasherType, type[PasswordHasher]] = {}

    @classmethod
    def get(cls, password_hasher_type: PasswordHasherType | None = None) -> PasswordHasher:
        if not password_hasher_type:
            password_hasher_type = settings.system.default_password_hasher_type
        password_hasher = cls._hashers.get(password_hasher_type)
        if not password_hasher:
            raise AccessControlException(SystemMessages.PASSWORD_HASHER_NOT_REGISTERED)
        return password_hasher()

    @classmethod
    def register(cls, password_hasher_type: PasswordHasherType, password_hasher: type[PasswordHasher]) -> None:
        cls._hashers[password_hasher_type] = password_hasher
