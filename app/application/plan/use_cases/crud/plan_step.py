from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.plan.entities.plan_step import PlanStepEntity
from domain.plan.repositories.plan import PlanStepFilter


class PlanStepCrudUseCase(BaseCrudUseCase[PlanStepEntity, PlanStepFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(PlanStepEntity, PlanStepFilter, account=account)

