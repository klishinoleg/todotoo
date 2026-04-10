from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.idea_event.entities.idea_event import IdeaEventEntity
from domain.idea_event.repositories.event import IdeaEventFilter, IdeaEventRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea_event.idea_event import IdeaEventModel


class IdeaEventTortoiseRepository(
    IdeaEventRepository[QuerySet],
    BaseTortoiseRepository[IdeaEventEntity, IdeaEventFilter[QuerySet], IdeaEventModel],
):
    model: Type[IdeaEventModel] = IdeaEventModel
    entity_cls: Type[IdeaEventEntity] = IdeaEventEntity

    async def to_entity(self, model: IdeaEventModel) -> IdeaEventEntity:
        return IdeaEventEntity(
            id=model.id,
            idea_id=model.idea_id,
            title=model.title,
            description=model.description,
            start_datetime=model.start_datetime,
            end_datetime=model.end_datetime,
            capacity=model.capacity,
            is_free_join=model.is_free_join,
            location_name=model.location_name,
            latitude=model.latitude,
            longitude=model.longitude,
            cover_image=model.cover_image,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: IdeaEventEntity) -> IdeaEventModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "title": entity.title,
            "description": entity.description,
            "start_datetime": entity.start_datetime,
            "end_datetime": entity.end_datetime,
            "capacity": entity.capacity,
            "is_free_join": entity.is_free_join,
            "location_name": entity.location_name,
            "latitude": entity.latitude,
            "longitude": entity.longitude,
            "cover_image": entity.cover_image,
            "created_by": entity.created_by,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaEventEntity, IdeaEventTortoiseRepository, RepositoryType.TORTOISE)

