from abc import ABC
from collections import defaultdict
from typing import Type, cast

from core.enums.di.repository import RepositoryType, FilterFieldType
from domain.base.entity import BaseEntity
from domain.base.filters.base_filter import BaseFilterField
from domain.base.repository import BaseRepository
from core.config.settings import settings
from core.exceptions.system import RepositoryException
from core.messages.system.no_localized_messages import SystemMessages
from infrastructure.repository.transaction import RepositoryTransactionManager


class DIRepository[BR: BaseRepository]:
    repositories: dict[RepositoryType, dict[str, type]] = defaultdict(dict)
    filters: dict[RepositoryType, dict[FilterFieldType, Type[BaseFilterField]]] = defaultdict(dict)

    @classmethod
    def register_filter[BF: BaseFilterField](
            cls, filter_field_type: FilterFieldType, filter_impl: Type[BF], repository_type: RepositoryType
    ) -> None:
        cls.filters[repository_type][filter_field_type] = filter_impl

    @classmethod
    def register[T: BaseEntity](
            cls,
            entity_cls: Type[T],
            repo_cls: Type[BR],
            repository_type: RepositoryType,
    ) -> None:
        """
        Register a repository instance for a specific type (TORTOISE, MOCK).
        """
        domain_cls = entity_cls.__name__
        cls.repositories[repository_type][domain_cls] = repo_cls

    @classmethod
    def get(
            cls,
            entity_cls: Type[BaseEntity],
            repository_type: RepositoryType | None = None,
    ) -> BR:
        """
        Resolve concrete repository implementation by type.
        """
        if not repository_type:
            repository_type = settings.system.default_repository_type
        repositories = cls.repositories.get(repository_type)
        if not repositories:
            raise RepositoryException(SystemMessages.UNKNOWN_REPOSITORY_TYPE)

        repo_impl = repositories.get(entity_cls.__name__)
        if not repo_impl:
            raise RepositoryException(SystemMessages.REPOSITORY_NOT_REGISTERED)
        return cast(BR, repo_impl())

    @classmethod
    def get_filter[BF: BaseFilterField](
            cls, filter_field_type: FilterFieldType,
            repository_type: RepositoryType = settings.system.default_repository_type
    ) -> Type[BF]:
        filters = cls.filters.get(repository_type)
        if not filters:
            raise RepositoryException(SystemMessages.UNKNOWN_REPOSITORY_TYPE)
        filter_impl_cls = filters.get(filter_field_type)
        if not filter_impl_cls:
            raise RepositoryException(SystemMessages.FILTER_NOT_REGISTERED)
        return cast(Type[BF], filter_impl_cls)


class DIRepositoryTransaction:
    _registry: dict[RepositoryType, type[RepositoryTransactionManager]] = {}

    @classmethod
    def register(cls, manager_type: RepositoryType, manager_impl: type[RepositoryTransactionManager]) -> None:
        cls._registry[manager_type] = manager_impl

    @classmethod
    def get(cls, manager_type: RepositoryType | None = None) -> RepositoryTransactionManager:
        if manager_type is None:
            manager_type = settings.system.default_repository_type

        impl = cls._registry.get(manager_type)
        if not impl:
            raise RepositoryException(SystemMessages.REPOSITORY_TRANSACTION_MANAGER_NOT_REGISTERED)
        return impl()
