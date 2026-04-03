from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea_participant.entities.participation_request import ParticipationRequestEntity
from domain.idea_participant.repositories.idea_participant import ParticipationRequestFilter


class ParticipationRequestCrudUseCase(BaseCrudUseCase[ParticipationRequestEntity, ParticipationRequestFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(ParticipationRequestEntity, ParticipationRequestFilter, account=account)

