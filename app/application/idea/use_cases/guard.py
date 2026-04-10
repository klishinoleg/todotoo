from core.enums.system.error_fields import ErrorFields
from core.enums.app.idea_participant.idea_role import IdeaRoleEnum
from core.enums.app.idea_participant.participant_status import ParticipantStatusEnum
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException
from infrastructure.repository.tortoise.models.idea_participant.idea_participant import IdeaParticipantModel


async def ensure_idea_admin(account: AccountEntity | None, idea_id: int) -> None:
    if account is None or account.id is None:
        raise DomainValidationException("Authentication required", field=ErrorFields.ACCOUNT)

    participant = await IdeaParticipantModel.filter(
        idea_id=idea_id,
        account_id=account.id,
        role=str(IdeaRoleEnum.ADMIN),
        status=str(ParticipantStatusEnum.ACTIVE),
    ).first()
    if participant is not None:
        return
    raise DomainValidationException("Only idea admin can perform this action", field=ErrorFields.DETAILS)


async def ensure_idea_participant(account: AccountEntity | None, idea_id: int) -> None:
    if account is None or account.id is None:
        raise DomainValidationException("Authentication required", field=ErrorFields.ACCOUNT)

    participant = await IdeaParticipantModel.filter(
        idea_id=idea_id,
        account_id=account.id,
        status=str(ParticipantStatusEnum.ACTIVE),
    ).first()
    if participant is not None:
        return
    raise DomainValidationException("Only active idea participant can perform this action", field=ErrorFields.DETAILS)
