from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea_event.entities.event_reaction import IdeaEventReactionEntity
from domain.idea_event.repositories.event import IdeaEventReactionFilter


class IdeaEventReactionCrudUseCase(BaseCrudUseCase[IdeaEventReactionEntity, IdeaEventReactionFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaEventReactionEntity, IdeaEventReactionFilter, account=account)

