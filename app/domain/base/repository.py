from abc import ABC, abstractmethod
from typing import Set

from domain.base.entity import BaseEntity
from domain.base.filters.base_filter import BaseFilter


class BaseRepository[T: BaseEntity, FD: BaseFilter](ABC):
    """
    Abstract base repository for domain entities.

    This interface defines persistence operations that concrete infrastructure
    repositories (e.g., Tortoise ORM, SQLAlchemy, Redis, MongoDB) must implement.

    The repository works on:
        - T: Domain entity type
        - FD: Domain filter type (DTO describing filtering params)

    Notes:
        - All operations are async because the infrastructure layer is async (DB, I/O)
        - Domain layer depends only on this abstraction, not on ORM details
        - Pagination and ordering are optional and controlled at the repository level
    """

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    @abstractmethod
    async def get(self, entity_id: int) -> T | None:
        """
        Retrieve a single entity by its ID.

        Args:
            entity_id: Primary key value.

        Returns:
            Entity instance or None if not found.
        """
        ...

    @abstractmethod
    async def get_many(self, ids: list[int]) -> list[T]:
        """
        Retrieve multiple entities by list of IDs.

        Args:
            ids: List of primary keys.

        Returns:
            List of entity instances (order not guaranteed).
        """
        ...

    @abstractmethod
    async def save(self, entity: T, update_fields: Set[str] | None = None) -> T:
        """
        Persist changes of an existing entity.

        Args:
            :param entity: Entity with modified fields.
            :param update_fields:

        Returns:
            Updated entity as stored in DB.

        """
        ...

    @abstractmethod
    async def create(self, entity: T) -> T:
        """
        Insert a new entity into storage.

        Args:
            entity: Entity without ID (id=None).

        Returns:
            Entity with an assigned primary key.
        """
        ...

    @abstractmethod
    async def bulk_create(self, entities: list[T]) -> list[T]:
        """
        Insert multiple entities in a single operation.

        Args:
            entities: List of new entities (id=None).

        Returns:
            List of persisting entities with assigned IDs.
        """
        ...

    # ---------------------------------------------------------
    # FILTERED LIST & PAGINATION
    # ---------------------------------------------------------

    @abstractmethod
    async def filtered_list(
            self,
            filter_data: FD,
    ) -> list[T]:
        """
        Return a list of entities matching domain-level filter definition.

        Args:
            :param filter_data:
                Domain filter DTO containing field-level filters.
                Each filter must implement BaseFilterField.extend_query() logic
                in the infrastructure repository.

        Returns:
            List of entities after filtering, ordering and pagination.
        """
        ...
