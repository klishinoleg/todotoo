from application.event.use_cases.crud.event_member import EventMemberCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class EventMemberRouter(V1CrudRouter[EventMemberCrudUseCase]):
    prefix = "/event-members"
    tags = ["v1/event"]
    use_case_cls = EventMemberCrudUseCase


event_member_crud_router = EventMemberRouter()
router = event_member_crud_router.router

