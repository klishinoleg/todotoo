from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.idea_participant.idea_role import IdeaRoleEnum
from core.enums.app.idea_participant.participant_status import ParticipantStatusEnum
from domain.idea_participant.entities.idea_participant import IdeaParticipantEntity
from domain.idea_participant.repositories.idea_participant import IdeaParticipantFilter, IdeaParticipantRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea_participant.idea_participant import IdeaParticipantModel


class IdeaParticipantTortoiseRepository(
    IdeaParticipantRepository[QuerySet],
    BaseTortoiseRepository[IdeaParticipantEntity, IdeaParticipantFilter[QuerySet], IdeaParticipantModel],
):
    model: Type[IdeaParticipantModel] = IdeaParticipantModel
    entity_cls: Type[IdeaParticipantEntity] = IdeaParticipantEntity

    async def to_entity(self, model: IdeaParticipantModel) -> IdeaParticipantEntity:
        return IdeaParticipantEntity(
            id=model.id,
            idea_id=model.idea_id,
            account_id=model.account_id,
            role=IdeaRoleEnum(model.role),
            status=ParticipantStatusEnum(model.status),
            joined_at=model.joined_at,
            invited_by=model.invited_by,
        )

    def from_entity(self, entity: IdeaParticipantEntity) -> IdeaParticipantModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "account_id": entity.account_id,
            "role": str(entity.role),
            "status": str(entity.status),
            "joined_at": entity.joined_at,
            "invited_by": entity.invited_by,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaParticipantEntity, IdeaParticipantTortoiseRepository, RepositoryType.TORTOISE)

