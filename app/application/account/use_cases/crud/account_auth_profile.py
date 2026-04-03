from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.account.repositories.account_auth_profile import AccountAuthProfileFilter


class AccountAuthProfileCrudUseCase(BaseCrudUseCase[AccountAuthProfileEntity, AccountAuthProfileFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(AccountAuthProfileEntity, AccountAuthProfileFilter, account=account)

