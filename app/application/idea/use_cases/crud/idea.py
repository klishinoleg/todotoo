from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea.entities.idea import IdeaEntity
from domain.idea.repositories.idea import IdeaFilter


class IdeaCrudUseCase(BaseCrudUseCase[IdeaEntity, IdeaFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaEntity, IdeaFilter, account=account)

