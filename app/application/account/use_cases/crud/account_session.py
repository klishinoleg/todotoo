from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.account.entities.account_session import AccountSessionEntity
from domain.account.repositories.account_session import AccountSessionFilter


class AccountSessionCrudUseCase(BaseCrudUseCase[AccountSessionEntity, AccountSessionFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(AccountSessionEntity, AccountSessionFilter, account=account)

