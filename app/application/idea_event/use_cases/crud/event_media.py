from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea_event.entities.event_media import IdeaEventMediaEntity
from domain.idea_event.repositories.event import IdeaEventMediaFilter


class IdeaEventMediaCrudUseCase(BaseCrudUseCase[IdeaEventMediaEntity, IdeaEventMediaFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaEventMediaEntity, IdeaEventMediaFilter, account=account)

