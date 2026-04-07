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
        await new_model.save(force_create=True)
        return await self.to_entity(new_model)

    async def bulk_create(self, entities: list[T]) -> list[T]:
        models = [self.from_entity(e) for e in entities]
        await self.model.bulk_create(models)
        return [await self.to_entity(m) for m in models]

    async def save(self, entity: T, update_fields: Set[str] | None = None) -> T:
        not_saved_model = self.from_entity(entity)
        await not_saved_model.save(update_fields=update_fields)
        model = await self.model.get(id=entity.id)
        return await self.to_entity(model)

    async def delete(self, entity_id: int) -> bool:
        deleted_count = await self.model.filter(id=entity_id).delete()
        return deleted_count > 0

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
        query = self._apply_order_and_pagination(query, filter_data, with_pagination=True)
        models = await query
        return [await self.to_entity(m) for m in models]

    async def filtered_count(self, filter_data: FD) -> int:
        query = self.model.all()
        query = filter_data.extend_query(query)
        return await query.count()

    @staticmethod
    def _apply_order_and_pagination(query: QuerySet, filter_data: FD, with_pagination: bool) -> QuerySet:
        if filter_data.order_data:
            query = query.order_by(*filter_data.order_data)

        if with_pagination and filter_data.page and filter_data.per_page:
            offset = max((filter_data.page - 1) * filter_data.per_page, 0)
            query = query.offset(offset).limit(filter_data.per_page)

        return query

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
