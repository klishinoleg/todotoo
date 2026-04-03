from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea_event.entities.event_participant import IdeaEventParticipantEntity
from domain.idea_event.repositories.event import IdeaEventParticipantFilter


class IdeaEventParticipantCrudUseCase(BaseCrudUseCase[IdeaEventParticipantEntity, IdeaEventParticipantFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaEventParticipantEntity, IdeaEventParticipantFilter, account=account)

