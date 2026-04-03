from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea_participant.entities.idea_participant import IdeaParticipantEntity
from domain.idea_participant.repositories.idea_participant import IdeaParticipantFilter


class IdeaParticipantCrudUseCase(BaseCrudUseCase[IdeaParticipantEntity, IdeaParticipantFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaParticipantEntity, IdeaParticipantFilter, account=account)

