from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.event.entities.event_occurrence_message import EventOccurrenceMessageEntity
from domain.event.repositories.event_occurrence_message import (
    EventOccurrenceMessageFilter,
    EventOccurrenceMessageRepository,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.event.event_occurrence_message import (
    EventOccurrenceMessageModel,
)


class EventOccurrenceMessageTortoiseRepository(
    EventOccurrenceMessageRepository[QuerySet],
    BaseTortoiseRepository[
        EventOccurrenceMessageEntity,
        EventOccurrenceMessageFilter[QuerySet],
        EventOccurrenceMessageModel,
    ],
):
    """
    Tortoise ORM repository for EventOccurrenceMessageEntity.
    """

    model: Type[EventOccurrenceMessageModel] = EventOccurrenceMessageModel
    entity_cls: Type[EventOccurrenceMessageEntity] = EventOccurrenceMessageEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(
        self, model: EventOccurrenceMessageModel
    ) -> EventOccurrenceMessageEntity:
        return EventOccurrenceMessageEntity(
            id=model.id,
            event_occurrence_id=model.event_occurrence_id,
            parent_message_id=model.parent_message_id,
            event_id=model.event_id,
            event_member_id=model.event_member_id,
            text=model.text,
            image=model.image,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model
    # ---------------------------------------
    def from_entity(
        self, entity: EventOccurrenceMessageEntity
    ) -> EventOccurrenceMessageModel:
        return self.model(
            id=entity.id,
            event_occurrence_id=entity.event_occurrence_id,
            parent_message_id=entity.parent_message_id,
            event_id=entity.event_id,
            event_member_id=entity.event_member_id,
            text=entity.text,
            image=entity.image,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


# Register repository implementation in DI
DIRepository.register(
    EventOccurrenceMessageEntity,
    EventOccurrenceMessageTortoiseRepository,
    RepositoryType.TORTOISE,
)