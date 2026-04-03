from application.plan.use_cases.crud.plan import PlanCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class PlanRouter(V1CrudRouter[PlanCrudUseCase]):
    prefix = "/plans"
    tags = ["v1/plan"]
    use_case_cls = PlanCrudUseCase


plan_crud_router = PlanRouter()
router = plan_crud_router.router

