from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.plan.entities.plan import PlanEntity
from domain.plan.repositories.plan import PlanFilter


class PlanCrudUseCase(BaseCrudUseCase[PlanEntity, PlanFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(PlanEntity, PlanFilter, account=account)

