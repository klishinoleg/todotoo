from typing import Any

from application.base.use_case.crud import BaseCrudUseCase
from application.idea.use_cases.guard import ensure_idea_admin
from core.di.repository import DIRepositoryTransaction
from core.enums.app.activity_log.idea_activity_type import IdeaActivityTypeEnum
from core.enums.app.idea_participant.idea_role import IdeaRoleEnum
from core.enums.app.idea_participant.participant_status import ParticipantStatusEnum
from core.enums.system.error_fields import ErrorFields
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException
from domain.idea.entities.idea import IdeaEntity
from domain.idea.repositories.idea import IdeaFilter
from infrastructure.repository.tortoise.models.activity_log.idea_activity import IdeaActivityModel
from infrastructure.repository.tortoise.models.idea_participant.idea_participant import IdeaParticipantModel


class IdeaCrudUseCase(BaseCrudUseCase[IdeaEntity, IdeaFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaEntity, IdeaFilter, account=account)

    async def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self.account is None or self.account.id is None:
            raise DomainValidationException("Authentication required", field=ErrorFields.ACCOUNT)

        create_payload: dict[str, Any] = dict(payload)
        create_payload["creator_id"] = self.account.id
        create_payload.pop("id", None)
        try:
            entity = self._entity_cls(**create_payload)
        except TypeError as exc:
            raise DomainValidationException(str(exc), field=ErrorFields.DETAILS)

        tx = DIRepositoryTransaction.get().start()
        async with tx:
            created = await self._service.create(entity)
            if created.id is None:
                raise DomainValidationException("Failed to persist idea", field=ErrorFields.DETAILS)
            await IdeaParticipantModel.create(
                idea_id=created.id,
                account_id=self.account.id,
                role=str(IdeaRoleEnum.ADMIN),
                status=str(ParticipantStatusEnum.ACTIVE),
                invited_by=self.account.id,
            )
            await IdeaActivityModel.create(
                idea_id=created.id,
                account_id=self.account.id,
                type=str(IdeaActivityTypeEnum.IDEA_CREATED),
                payload={"idea_title": created.title},
            )
        return self._serialize_entity(created)

    async def update(self, entity_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        await ensure_idea_admin(self.account, entity_id)
        allowed = {"title", "description", "slogan", "cover_image", "visibility", "status", "is_active"}
        sanitized = {k: v for k, v in payload.items() if k in allowed}
        return await super().update(entity_id, sanitized)

    async def delete(self, entity_id: int) -> bool:
        await ensure_idea_admin(self.account, entity_id)
        return await super().delete(entity_id)
