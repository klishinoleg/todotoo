from abc import ABC, abstractmethod
from typing import Type, Set

from tortoise.exceptions import DoesNotExist
from tortoise.queryset import QuerySet

from domain.base.entity import BaseEntity
from domain.base.filters.base_filter import BaseFilter
from domain.base.repository import BaseRepository
from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class BaseTortoiseRepository[T: BaseEntity, FD: BaseFilter[QuerySet], TM: BaseTortoiseModel](BaseRepository[T, FD],
                                                                                             ABC):
    """
    Universal Tortoise ORM repository implementing BaseRepository.

    Requirements:
        - TM: Tortoise model
        - T: Domain entity
        - FD: Filter DTO
    """

    model: Type[TM]  # Tortoise Model class
    entity_cls: Type[T]  # Domain entity class

    # ------------------------ CRUD ------------------------

    async def get(self, entity_id: int) -> T | None:
        try:
            model = await self.model.get(id=entity_id)
        except DoesNotExist:
            return None
        return await self.to_entity(model)

    async def get_many(self, ids: list[int]) -> list[T]:
        models = await self.model.filter(id__in=ids)
        return [await self.to_entity(m) for m in models]

    async def create(self, entity: T) -> T:
        new_model = self.from_entity(entity)
        model = await new_model.create()
        return await self.to_entity(model)

    async def bulk_create(self, entities: list[T]) -> list[T]:
        models = [self.from_entity(e) for e in entities]
        await self.model.bulk_create(models)
        return [await self.to_entity(m) for m in models]

    async def save(self, entity: T, update_fields: Set[str] | None = None) -> T:
        not_saved_model = self.from_entity(entity)
        await not_saved_model.save(update_fields=update_fields)
        model = await self.model.get(id=entity.id)
        return await self.to_entity(model)

    # ------------------------ FILTERS ------------------------

    async def filtered_list(self, filter_data: FD) -> list[T]:
        """
        Generic filtering:
            - Iterates over filter_data fields
            - Applies BaseFilterField.extend_query()
            - Converts Tortoise model → domain entity
        """
        query = self.model.all()
        query = filter_data.extend_query(query)
        models = await query
        return [await self.to_entity(m) for m in models]

    # ------------------------ Mapping ------------------------

    @abstractmethod
    async def to_entity(self, model: TM) -> T:
        """
        Convert Tortoise model to domain entity.
        Override if mapping is more complex.
        """
        ...

    @abstractmethod
    def from_entity(self, entity: T) -> TM:
        """
        Convert domain entity to primitive dict for Tortoise ORM.
        """
        ...
