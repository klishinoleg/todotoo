from application.idea_event.use_cases.crud.idea_event import IdeaEventCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaEventRouter(V1CrudRouter[IdeaEventCrudUseCase]):
    prefix = "/idea-events"
    tags = ["v1/idea_event"]
    use_case_cls = IdeaEventCrudUseCase


idea_event_crud_router = IdeaEventRouter()
router = idea_event_crud_router.router

