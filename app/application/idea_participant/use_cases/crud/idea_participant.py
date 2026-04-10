from typing import Any

from application.base.use_case.crud import BaseCrudUseCase
from application.idea.use_cases.guard import ensure_idea_admin
from core.enums.app.activity_log.idea_activity_type import IdeaActivityTypeEnum
from core.enums.system.error_fields import ErrorFields
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException
from domain.idea_participant.entities.idea_participant import IdeaParticipantEntity
from domain.idea_participant.repositories.idea_participant import IdeaParticipantFilter
from infrastructure.repository.tortoise.models.activity_log.idea_activity import IdeaActivityModel


class IdeaParticipantCrudUseCase(BaseCrudUseCase[IdeaParticipantEntity, IdeaParticipantFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaParticipantEntity, IdeaParticipantFilter, account=account)

    async def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        raw_idea_id = payload.get("idea_id")
        if not isinstance(raw_idea_id, int):
            raise DomainValidationException("idea_id must be int", field=ErrorFields.DETAILS)
        idea_id = raw_idea_id
        await ensure_idea_admin(self.account, idea_id)
        return await super().create(payload)

    async def update(self, entity_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        current = await self._get_or_raise(entity_id)
        await ensure_idea_admin(self.account, current.idea_id)
        allowed = {"role", "status", "invited_by"}
        sanitized = {k: v for k, v in payload.items() if k in allowed}
        updated = await super().update(entity_id, sanitized)

        new_role_raw = sanitized.get("role")
        if new_role_raw is not None and str(current.role) != str(new_role_raw):
            await IdeaActivityModel.create(
                idea_id=current.idea_id,
                account_id=self.account.id if self.account else None,
                type=str(IdeaActivityTypeEnum.ROLE_CHANGED),
                payload={
                    "participant_id": entity_id,
                    "from_role": str(current.role),
                    "to_role": str(new_role_raw),
                },
            )

        return updated

    async def delete(self, entity_id: int) -> bool:
        current = await self._get_or_raise(entity_id)
        await ensure_idea_admin(self.account, current.idea_id)
        return await super().delete(entity_id)
