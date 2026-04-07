from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.event.entities.event_member import EventMemberEntity
from domain.event.repositories.event_member import (
    EventMemberFilter,
    EventMemberRepository,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.event.event_member import (
    EventMemberModel,
)


class EventMemberTortoiseRepository(
    EventMemberRepository[QuerySet],
    BaseTortoiseRepository[
        EventMemberEntity,
        EventMemberFilter[QuerySet],
        EventMemberModel,
    ],
):
    """
    Tortoise ORM repository for EventMemberEntity.
    """

    model: Type[EventMemberModel] = EventMemberModel
    entity_cls: Type[EventMemberEntity] = EventMemberEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(self, model: EventMemberModel) -> EventMemberEntity:
        return EventMemberEntity(
            id=model.id,
            event_occurrence_id=model.event_occurrence_id,
            event_id=model.event_id,
            account_id=model.account_id,
            has_accepted=model.has_accepted,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model
    # ---------------------------------------
    def from_entity(self, entity: EventMemberEntity) -> EventMemberModel:
        payload: dict[str, object] = {
            "event_occurrence_id": entity.event_occurrence_id,
            "event_id": entity.event_id,
            "account_id": entity.account_id,
            "has_accepted": entity.has_accepted,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


# Register repository implementation in DI
DIRepository.register(EventMemberEntity, EventMemberTortoiseRepository, RepositoryType.TORTOISE)
