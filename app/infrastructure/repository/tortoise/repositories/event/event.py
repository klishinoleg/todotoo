from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.storage import get_storage
from domain.event.entities.event import EventEntity
from domain.event.repositories.event import EventFilter, EventRepository
from infrastructure.repository.tortoise.base.geo.convert import (
    from_postgis_point,
    from_postgis_polygon,
    to_postgis_point,
    to_postgis_polygon,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.event.event import EventModel


class EventTortoiseRepository(
    EventRepository[QuerySet],
    BaseTortoiseRepository[EventEntity, EventFilter[QuerySet], EventModel],
):
    """
    Tortoise ORM repository for EventEntity.

    Uses:
        - PostGIS point & polygon for spatial filters
        - Storage URL resolver for media keys
    """

    model: Type[EventModel] = EventModel
    entity_cls: Type[EventEntity] = EventEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(self, model: EventModel) -> EventEntity:
        storage = get_storage()
        image = storage.get_url(model.image)
        return EventEntity(
            id=model.id,
            name=model.name,
            description=model.description,
            account_id=model.account_id,
            point=from_postgis_point(model.point),
            polygon=from_postgis_polygon(model.polygon),
            group_link=model.group_link,
            image=image,
            image_small=image,
            image_medium=image,
            image_large=image,
            chat_link=model.chat_link,
            schedule_rule_ids=[esr.id for esr in await model.schedule_rules.all()],
            location_id=model.location_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model
    # ---------------------------------------
    def from_entity(self, entity: EventEntity) -> EventModel:
        storage = get_storage()
        return self.model(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            account_id=entity.account_id,
            point=to_postgis_point(entity.point),
            polygon=to_postgis_polygon(entity.polygon),
            group_link=entity.group_link,
            image=storage.to_key(entity.image),
            chat_link=entity.chat_link,
            schedule_rules=entity.schedule_rule_ids,
            location_id=entity.location_id,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


# Register repository implementation in DI
DIRepository.register(EventEntity, EventTortoiseRepository, RepositoryType.TORTOISE)
