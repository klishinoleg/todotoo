from application.event.use_cases.crud.event import EventCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class EventRouter(V1CrudRouter[EventCrudUseCase]):
    prefix = "/events"
    tags = ["v1/event"]
    use_case_cls = EventCrudUseCase


event_crud_router = EventRouter()
router = event_crud_router.router

