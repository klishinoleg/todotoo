from typing import Type, Dict

from core.enums.app.account.auth_provider import AuthProviderType
from core.exceptions.system import AuthProviderException
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from core.messages.system.no_localized_messages import SystemMessages


class DIAuthProviderData:
    """
    DI container that maps AuthProviderType → BaseAuthProviderData implementation.

    The goal:
        - Hide provider-specific logic behind a unified interface
        - Select the correct ProviderData class at runtime (Telegram, Password, etc.)
        - Guarantee clean domain-level provider_data for AccountAuthProfileEntity
    """

    _provider_map: Dict[AuthProviderType | str, Type[BaseAuthProviderData]] = {}

    @classmethod
    def register(
            cls,
            provider_type: AuthProviderType | str,
            provider_data_cls: Type[BaseAuthProviderData]
    ) -> None:
        """
        Register a mapping for provider data model.
        """
        cls._provider_map[provider_type] = provider_data_cls

    @classmethod
    def get(
            cls,
            provider_type: AuthProviderType | str,
            provider_raw_validated_data: dict
    ) -> BaseAuthProviderData:
        """
        Instantiate a proper ProviderData object for a given provider type.
        """
        provider_cls = cls._provider_map.get(provider_type)
        if not provider_cls:
            raise AuthProviderException(SystemMessages.AUTH_PROVIDER_NOT_REGISTERED)

        return provider_cls(provider_raw_validated_data)
