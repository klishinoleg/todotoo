from application.idea.use_cases.crud.idea import IdeaCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaRouter(V1CrudRouter[IdeaCrudUseCase]):
    prefix = "/ideas"
    tags = ["v1/idea"]
    use_case_cls = IdeaCrudUseCase


idea_crud_router = IdeaRouter()
router = idea_crud_router.router

