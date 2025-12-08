from abc import ABC
from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.base.entity import BaseEntity
from domain.base.filters.base_filter import BaseFilter
from domain.base.repository import BaseRepository


class BaseService[T: BaseEntity, FD: BaseFilter](ABC):
    """
    Base application-level service.

    Responsibilities:
    - Resolve correct repository implementation via DI
    - Expose repository operations to upper layers (use cases)
    - Allow inherited services to add validation, caching, permissions, etc.

    Notes:
    - This class does NOT contain business logic by design.
    - This is a thin convenience wrapper over BaseRepository.
    """

    repository: BaseRepository[T, FD]

    def __init__(
            self,
            entity_cls: type[T],
            repository_type: RepositoryType | None = None,
    ):
        # Resolve concrete repo implementation
        self.repository = DIRepository.get(entity_cls, repository_type)

    # ---------------------------------------------------------
    # CRUD passthrough
    # ---------------------------------------------------------

    async def get(self, entity_id: int) -> T | None:
        return await self.repository.get(entity_id)

    async def get_many(self, ids: list[int]) -> list[T]:
        return await self.repository.get_many(ids)

    async def create(self, entity: T) -> T:
        return await self.repository.create(entity)

    async def save(self, entity: T) -> T:
        return await self.repository.save(entity)

    async def bulk_create(self, entities: list[T]) -> list[T]:
        return await self.repository.bulk_create(entities)

    # ---------------------------------------------------------
    # Filter + list passthrough
    # ---------------------------------------------------------

    async def filtered_list(self, filter_data: FD) -> list[T]:
        return await self.repository.filtered_list(filter_data)
