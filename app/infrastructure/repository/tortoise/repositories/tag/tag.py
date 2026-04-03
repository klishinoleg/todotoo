from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.storage import get_storage
from domain.tag.entities.tag import TagEntity
from domain.tag.repositories.tag import TagFilter, TagRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.tag.tag import TagModel


class TagTortoiseRepository(
    TagRepository[QuerySet],
    BaseTortoiseRepository[TagEntity, TagFilter[QuerySet], TagModel],
):
    """
    Tortoise ORM repository for TagEntity.
    """

    model: Type[TagModel] = TagModel
    entity_cls: Type[TagEntity] = TagEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(self, model: TagModel) -> TagEntity:
        storage = get_storage()
        icon = storage.get_url(model.icon)
        return TagEntity(
            id=model.id,
            name=model.name,
            slug=model.slug,
            parent_id=model.parent_id,
            ordering=model.ordering,
            is_active=model.is_active,
            icon=icon,
            icon_small=icon,
            icon_middle=icon,
        )

    # ---------------------------------------
    # Mapping: Entity → Model
    # ---------------------------------------
    def from_entity(self, entity: TagEntity) -> TagModel:
        storage = get_storage()
        return self.model(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            parent_id=entity.parent_id,
            ordering=entity.ordering,
            is_active=entity.is_active,
            icon=storage.to_key(entity.icon),
        )


# Register repository implementation in DI
DIRepository.register(TagEntity, TagTortoiseRepository, RepositoryType.TORTOISE)
