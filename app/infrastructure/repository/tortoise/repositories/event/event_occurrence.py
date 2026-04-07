from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.event.entities.event_occurrence import EventOccurrenceEntity
from domain.event.repositories.event_occurrence import (
    EventOccurrenceFilter,
    EventOccurrenceRepository,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.event.event_occurrence import (
    EventOccurrenceModel,
)


class EventOccurrenceTortoiseRepository(
    EventOccurrenceRepository[QuerySet],
    BaseTortoiseRepository[
        EventOccurrenceEntity,
        EventOccurrenceFilter[QuerySet],
        EventOccurrenceModel,
    ],
):
    """
    Tortoise ORM repository for EventOccurrenceEntity.
    """

    model: Type[EventOccurrenceModel] = EventOccurrenceModel
    entity_cls: Type[EventOccurrenceEntity] = EventOccurrenceEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(
        self, model: EventOccurrenceModel
    ) -> EventOccurrenceEntity:
        return EventOccurrenceEntity(
            id=model.id,
            event_id=model.event_id,
            start_at=model.start_at,
            end_at=model.end_at,
            members_count=model.members_count,
            location_id=model.location_id,
            is_canceled=model.is_canceled,
            is_finished=model.is_finished,
        )

    # ---------------------------------------
    # Mapping: Entity → Model
    # ---------------------------------------
    def from_entity(self, entity: EventOccurrenceEntity) -> EventOccurrenceModel:
        payload: dict[str, object] = {
            "event_id": entity.event_id,
            "start_at": entity.start_at,
            "end_at": entity.end_at,
            "members_count": entity.members_count,
            "location_id": entity.location_id,
            "is_canceled": entity.is_canceled,
            "is_finished": entity.is_finished,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


# Register repository implementation in DI
DIRepository.register(EventOccurrenceEntity, EventOccurrenceTortoiseRepository, RepositoryType.TORTOISE)
