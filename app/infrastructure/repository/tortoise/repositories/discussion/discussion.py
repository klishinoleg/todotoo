from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.discussion.entities.discussion import DiscussionEntity
from domain.discussion.repositories.discussion import DiscussionFilter, DiscussionRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.discussion.discussion import DiscussionModel


class DiscussionTortoiseRepository(
    DiscussionRepository[QuerySet],
    BaseTortoiseRepository[DiscussionEntity, DiscussionFilter[QuerySet], DiscussionModel],
):
    model: Type[DiscussionModel] = DiscussionModel
    entity_cls: Type[DiscussionEntity] = DiscussionEntity

    async def to_entity(self, model: DiscussionModel) -> DiscussionEntity:
        return DiscussionEntity(
            id=model.id,
            idea_id=model.idea_id,
            title=model.title,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: DiscussionEntity) -> DiscussionModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "title": entity.title,
            "created_by": entity.created_by,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(DiscussionEntity, DiscussionTortoiseRepository, RepositoryType.TORTOISE)

