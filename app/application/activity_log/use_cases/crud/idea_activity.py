from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.activity_log.entities.idea_activity import IdeaActivityEntity
from domain.activity_log.repositories.idea_activity import IdeaActivityFilter


class IdeaActivityCrudUseCase(BaseCrudUseCase[IdeaActivityEntity, IdeaActivityFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaActivityEntity, IdeaActivityFilter, account=account)

