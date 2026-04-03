from application.plan.use_cases.crud.plan_step import PlanStepCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class PlanStepRouter(V1CrudRouter[PlanStepCrudUseCase]):
    prefix = "/plan-steps"
    tags = ["v1/plan"]
    use_case_cls = PlanStepCrudUseCase


plan_step_crud_router = PlanStepRouter()
router = plan_step_crud_router.router

