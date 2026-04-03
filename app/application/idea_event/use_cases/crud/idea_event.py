from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea_event.entities.idea_event import IdeaEventEntity
from domain.idea_event.repositories.event import IdeaEventFilter


class IdeaEventCrudUseCase(BaseCrudUseCase[IdeaEventEntity, IdeaEventFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaEventEntity, IdeaEventFilter, account=account)

