from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.meeting.meeting_participant_status import MeetingParticipantStatusEnum
from domain.meeting.entities.meeting_participant import MeetingParticipantEntity
from domain.meeting.repositories.meeting import MeetingParticipantFilter, MeetingParticipantRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.meeting.meeting_participant import MeetingParticipantModel


class MeetingParticipantTortoiseRepository(
    MeetingParticipantRepository[QuerySet],
    BaseTortoiseRepository[
        MeetingParticipantEntity,
        MeetingParticipantFilter[QuerySet],
        MeetingParticipantModel,
    ],
):
    model: Type[MeetingParticipantModel] = MeetingParticipantModel
    entity_cls: Type[MeetingParticipantEntity] = MeetingParticipantEntity

    async def to_entity(self, model: MeetingParticipantModel) -> MeetingParticipantEntity:
        return MeetingParticipantEntity(
            id=model.id,
            meeting_id=model.meeting_id,
            account_id=model.account_id,
            status=MeetingParticipantStatusEnum(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: MeetingParticipantEntity) -> MeetingParticipantModel:
        payload: dict[str, object] = {
            "meeting_id": entity.meeting_id,
            "account_id": entity.account_id,
            "status": str(entity.status),
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(MeetingParticipantEntity, MeetingParticipantTortoiseRepository, RepositoryType.TORTOISE)

