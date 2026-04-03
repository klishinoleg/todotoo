from application.motivation.use_cases.crud.motivator import MotivatorCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class MotivatorRouter(V1CrudRouter[MotivatorCrudUseCase]):
    prefix = "/motivators"
    tags = ["v1/motivation"]
    use_case_cls = MotivatorCrudUseCase


motivator_crud_router = MotivatorRouter()
router = motivator_crud_router.router

