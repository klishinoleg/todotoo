from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.motivation.entities.motivator import MotivatorEntity
from domain.motivation.repositories.motivator import MotivatorFilter


class MotivatorCrudUseCase(BaseCrudUseCase[MotivatorEntity, MotivatorFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(MotivatorEntity, MotivatorFilter, account=account)

