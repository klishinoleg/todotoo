from collections import defaultdict
from typing import Type, cast

from core.enums.di.repository import RepositoryType
from domain.base.entity import BaseEntity
from domain.base.filters.base_filter import BaseFilterField
from domain.base.repository import BaseRepository
from core.config.settings import settings
from core.exceptions.system import RepositoryException
from core.messages.system.no_localized_messages import SystemMessages


class DIRepository:
    _repositories: dict[RepositoryType, dict[str, Type[BaseRepository]]] = defaultdict(dict)
    _filters: dict[RepositoryType, dict[str, Type[BaseFilterField]]] = defaultdict(dict)

    @classmethod
    def register_filter[BF: BaseFilterField](cls, filter_impl: Type[BF], repository_type: RepositoryType) -> None:
        domain_filter = filter_impl.__bases__[0]
        cls._filters[repository_type][domain_filter.__name__] = filter_impl

    @classmethod
    def register[T: BaseEntity, BR: BaseRepository](
            cls,
            entity_cls: Type[T],
            repo_cls: Type[BR],
            repository_type: RepositoryType,
    ) -> None:
        """
        Register a repository instance for a specific type (TORTOISE, MOCK).
        """
        domain_cls = entity_cls.__name__
        cls._repositories[repository_type][domain_cls] = repo_cls

    @classmethod
    def get(
            cls,
            entity_cls: Type[BaseEntity],
            repository_type: RepositoryType | None = None,
    ) -> BaseRepository:
        """
        Resolve concrete repository implementation by type.
        """
        if not repository_type:
            repository_type = settings.system.default_repository_type
        repositories = cls._repositories.get(repository_type)
        if not repositories:
            raise RepositoryException(SystemMessages.UNKNOWN_REPOSITORY_TYPE)

        repo_impl = repositories.get(entity_cls.__name__)
        if not repo_impl:
            raise RepositoryException(SystemMessages.REPOSITORY_NOT_REGISTERED)
        return repo_impl()

    @classmethod
    def get_filter[BF: BaseFilterField](
            cls, filter_cls: Type[BF], repository_type: RepositoryType = settings.system.default_repository_type
    ) -> Type[BF]:
        filters = cls._filters.get(repository_type)
        if not filters:
            raise RepositoryException(SystemMessages.UNKNOWN_REPOSITORY_TYPE)
        filter_impl_cls = filters.get(filter_cls.__name__)
        if not filter_impl_cls:
            raise RepositoryException(SystemMessages.FILTER_NOT_REGISTERED)
        return cast(Type[BF], filter_impl_cls)
