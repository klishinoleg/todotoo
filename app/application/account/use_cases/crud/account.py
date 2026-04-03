from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.account.repositories.account import AccountFilter


class AccountCrudUseCase(BaseCrudUseCase[AccountEntity, AccountFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(AccountEntity, AccountFilter, account=account)

