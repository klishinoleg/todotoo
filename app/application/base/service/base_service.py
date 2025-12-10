from abc import ABC
from typing import cast, Any, Set

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.base.entity import BaseEntity
from domain.base.filters.base_filter import BaseFilter
from domain.base.repository import BaseRepository


class BaseService[T: BaseEntity, FD: BaseFilter, BR: BaseRepository](ABC):
    """
    Base application-level service.

    Responsibilities:
    - Resolve correct repository implementation via DI
    - Expose repository operations to upper layers (use cases)
    - Allow inherited services to add validation, caching, permissions, etc.

    Notes:
    - This class does NOT contain business logic by design.
    - This is a thin convenience wrapper over BaseRepository.7
    """

    repository: BR

    def __init__(
            self,
            entity_cls: type[T],
            repository_type: RepositoryType | None = None,
    ):
        # Resolve concrete repo implementation
        self.repository = DIRepository[BR].get(entity_cls, repository_type)

    # ---------------------------------------------------------
    # CRUD passthrough
    # ---------------------------------------------------------

    async def get(self, entity_id: int) -> T | None:
        return await self.repository.get(entity_id)

    async def get_many(self, ids: list[int]) -> list[T]:
        return await self.repository.get_many(ids)

    async def create(self, entity: T) -> T:
        result = await self.repository.create(entity)
        return cast(T, result)

    async def save(self, entity: T, update_fields: Set[str] | None = None) -> T:
        result = await self.repository.save(entity, update_fields=update_fields)
        return cast(T, result)

    async def bulk_create(self, entities: list[T]) -> list[T]:
        return await self.repository.bulk_create(entities)

    # ---------------------------------------------------------
    # Filter + list passthrough
    # ---------------------------------------------------------

    async def filtered_list(self, filter_data: FD) -> list[T]:
        return await self.repository.filtered_list(filter_data)
