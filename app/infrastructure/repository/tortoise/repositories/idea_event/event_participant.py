from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.idea_event.event_participant_status import EventParticipantStatusEnum
from domain.idea_event.entities.event_participant import IdeaEventParticipantEntity
from domain.idea_event.repositories.event import IdeaEventParticipantFilter, IdeaEventParticipantRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea_event.event_participant import IdeaEventParticipantModel


class IdeaEventParticipantTortoiseRepository(
    IdeaEventParticipantRepository[QuerySet],
    BaseTortoiseRepository[
        IdeaEventParticipantEntity,
        IdeaEventParticipantFilter[QuerySet],
        IdeaEventParticipantModel,
    ],
):
    model: Type[IdeaEventParticipantModel] = IdeaEventParticipantModel
    entity_cls: Type[IdeaEventParticipantEntity] = IdeaEventParticipantEntity

    async def to_entity(self, model: IdeaEventParticipantModel) -> IdeaEventParticipantEntity:
        return IdeaEventParticipantEntity(
            id=model.id,
            event_id=model.event_id,
            account_id=model.account_id,
            status=EventParticipantStatusEnum(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: IdeaEventParticipantEntity) -> IdeaEventParticipantModel:
        payload: dict[str, object] = {
            "event_id": entity.event_id,
            "account_id": entity.account_id,
            "status": str(entity.status),
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaEventParticipantEntity, IdeaEventParticipantTortoiseRepository, RepositoryType.TORTOISE)

