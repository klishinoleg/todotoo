from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.idea_participant.request_status import RequestStatusEnum
from domain.idea_participant.entities.participation_request import ParticipationRequestEntity
from domain.idea_participant.repositories.idea_participant import ParticipationRequestFilter, ParticipationRequestRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea_participant.participation_request import ParticipationRequestModel


class ParticipationRequestTortoiseRepository(
    ParticipationRequestRepository[QuerySet],
    BaseTortoiseRepository[
        ParticipationRequestEntity,
        ParticipationRequestFilter[QuerySet],
        ParticipationRequestModel,
    ],
):
    model: Type[ParticipationRequestModel] = ParticipationRequestModel
    entity_cls: Type[ParticipationRequestEntity] = ParticipationRequestEntity

    async def to_entity(self, model: ParticipationRequestModel) -> ParticipationRequestEntity:
        return ParticipationRequestEntity(
            id=model.id,
            idea_id=model.idea_id,
            account_id=model.account_id,
            message=model.message,
            status=RequestStatusEnum(model.status),
            reviewed_by=model.reviewed_by,
            reviewed_at=model.reviewed_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: ParticipationRequestEntity) -> ParticipationRequestModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "account_id": entity.account_id,
            "message": entity.message,
            "status": str(entity.status),
            "reviewed_by": entity.reviewed_by,
            "reviewed_at": entity.reviewed_at,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(ParticipationRequestEntity, ParticipationRequestTortoiseRepository, RepositoryType.TORTOISE)

