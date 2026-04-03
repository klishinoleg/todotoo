from core.config.settings import settings
from core.enums.di.storage import StorageType
from core.exceptions.system import RepositoryException
from core.messages.system.no_localized_messages import SystemMessages
from interfaces.storage.storage import Storage


class DIStorageProvider:
    _providers: dict[StorageType, type[Storage]] = {}

    @classmethod
    def register(cls, storage_type: StorageType, provider: type[Storage]) -> None:
        cls._providers[storage_type] = provider

    @classmethod
    def get(cls, storage_type: StorageType | None = None) -> Storage:
        if storage_type is None:
            storage_type = settings.storage.type

        provider_cls = cls._providers.get(storage_type)
        if provider_cls is None:
            raise RepositoryException(SystemMessages.STORAGE_PROVIDER_NOT_REGISTERED)
        return provider_cls()
