from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.idea_event.media_type import MediaTypeEnum
from domain.idea_event.entities.event_media import IdeaEventMediaEntity
from domain.idea_event.repositories.event import IdeaEventMediaFilter, IdeaEventMediaRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea_event.event_media import IdeaEventMediaModel


class IdeaEventMediaTortoiseRepository(
    IdeaEventMediaRepository[QuerySet],
    BaseTortoiseRepository[IdeaEventMediaEntity, IdeaEventMediaFilter[QuerySet], IdeaEventMediaModel],
):
    model: Type[IdeaEventMediaModel] = IdeaEventMediaModel
    entity_cls: Type[IdeaEventMediaEntity] = IdeaEventMediaEntity

    async def to_entity(self, model: IdeaEventMediaModel) -> IdeaEventMediaEntity:
        return IdeaEventMediaEntity(
            id=model.id,
            event_id=model.event_id,
            type=MediaTypeEnum(model.type),
            url=model.url,
            preview_url=model.preview_url,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: IdeaEventMediaEntity) -> IdeaEventMediaModel:
        payload: dict[str, object] = {
            "event_id": entity.event_id,
            "type": str(entity.type),
            "url": entity.url,
            "preview_url": entity.preview_url,
            "created_by": entity.created_by,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaEventMediaEntity, IdeaEventMediaTortoiseRepository, RepositoryType.TORTOISE)

