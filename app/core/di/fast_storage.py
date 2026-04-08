from core.config.settings import settings
from core.enums.di.fast_storage import FastStorageType
from core.exceptions.system import RepositoryException
from core.messages.system.no_localized_messages import SystemMessages
from interfaces.fast_storage.fast_storage import FastStorage


class DIFastStorageProvider:
    _providers: dict[FastStorageType, type[FastStorage]] = {}

    @classmethod
    def register(cls, storage_type: FastStorageType, provider: type[FastStorage]) -> None:
        cls._providers[storage_type] = provider

    @classmethod
    def get(cls, storage_type: FastStorageType | None = None) -> FastStorage:
        if storage_type is None:
            storage_type = settings.fast_storage.type

        provider_cls = cls._providers.get(storage_type)
        if provider_cls is None:
            raise RepositoryException(SystemMessages.FAST_STORAGE_PROVIDER_NOT_REGISTERED)
        return provider_cls()
