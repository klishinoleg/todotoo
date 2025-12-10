from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, Type


@dataclass(kw_only=True)
class BaseAuthProviderData(ABC):
    """
    Domain-level interface for provider-specific identity data.
    Each provider data object knows how to extract unified account fields.
    """
    provider_id_type: Type[str] | Type[int] = str
    _provider_raw_data: dict

    def __init__(self, provider_raw_data: dict) -> None:
        self._provider_raw_data = provider_raw_data

    def serialize(self) -> dict:
        return self._provider_raw_data

    @abstractmethod
    def is_valid(self) -> bool:
        """Check a signature or else validate the data is valid."""
        ...

    @abstractmethod
    def prepare_for_storage(self) -> Self:
        ...

    @abstractmethod
    def get_user_id(self) -> str | int:
        """Unique ID from provider."""
        ...

    @abstractmethod
    def get_username(self) -> str:
        ...

    @abstractmethod
    def get_public_name(self) -> str | None:
        ...

    @abstractmethod
    def get_is_premium(self) -> bool:
        ...

    @abstractmethod
    def get_language_code(self) -> str | None:
        ...

    @abstractmethod
    async def get_image_url(self) -> str | None:
        ...

    @abstractmethod
    def get_contact_url(self) -> str | None:
        ...
