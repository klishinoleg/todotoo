from typing import Any

from application.base.use_case.crud import BaseCrudUseCase
from application.idea.use_cases.guard import ensure_idea_admin
from core.di.repository import DIRepositoryTransaction
from core.enums.app.activity_log.idea_activity_type import IdeaActivityTypeEnum
from core.enums.app.idea_participant.idea_role import IdeaRoleEnum
from core.enums.app.idea_participant.participant_status import ParticipantStatusEnum
from core.enums.app.idea_participant.request_status import RequestStatusEnum
from domain.account.entities.account import AccountEntity
from domain.idea_participant.entities.participation_request import ParticipationRequestEntity
from domain.idea_participant.repositories.idea_participant import ParticipationRequestFilter
from infrastructure.repository.tortoise.models.activity_log.idea_activity import IdeaActivityModel
from infrastructure.repository.tortoise.models.idea_participant.idea_participant import IdeaParticipantModel


class ParticipationRequestCrudUseCase(BaseCrudUseCase[ParticipationRequestEntity, ParticipationRequestFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(ParticipationRequestEntity, ParticipationRequestFilter, account=account)

    async def update(self, entity_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        current = await self._get_or_raise(entity_id)
        await ensure_idea_admin(self.account, current.idea_id)
        allowed = {"status", "reviewed_by", "reviewed_at"}
        sanitized = {k: v for k, v in payload.items() if k in allowed}

        status = sanitized.get("status")
        if status is None:
            return await super().update(entity_id, sanitized)

        if str(status) != str(RequestStatusEnum.APPROVED):
            return await super().update(entity_id, sanitized)

        tx = DIRepositoryTransaction.get().start()
        async with tx:
            updated = await super().update(entity_id, sanitized)
            await self._ensure_participant_exists(current.idea_id, current.account_id)
            await IdeaActivityModel.create(
                idea_id=current.idea_id,
                account_id=self.account.id if self.account else None,
                type=str(IdeaActivityTypeEnum.REQUEST_APPROVED),
                payload={"request_id": entity_id, "account_id": current.account_id},
            )
            return updated

    async def _ensure_participant_exists(self, idea_id: int, account_id: int) -> None:
        existing = await IdeaParticipantModel.filter(idea_id=idea_id, account_id=account_id).first()
        if existing is not None:
            existing.status = str(ParticipantStatusEnum.ACTIVE)
            await existing.save(update_fields=["status"])
            return

        await IdeaParticipantModel.create(
            idea_id=idea_id,
            account_id=account_id,
            role=str(IdeaRoleEnum.VIEWER),
            status=str(ParticipantStatusEnum.ACTIVE),
            invited_by=self.account.id if self.account else None,
        )
