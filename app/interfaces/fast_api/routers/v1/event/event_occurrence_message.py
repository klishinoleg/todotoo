from application.event.use_cases.crud.event_occurrence_message import EventOccurrenceMessageCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class EventOccurrenceMessageRouter(V1CrudRouter[EventOccurrenceMessageCrudUseCase]):
    prefix = "/event-occurrence-messages"
    tags = ["v1/event"]
    use_case_cls = EventOccurrenceMessageCrudUseCase


event_occurrence_message_crud_router = EventOccurrenceMessageRouter()
router = event_occurrence_message_crud_router.router

