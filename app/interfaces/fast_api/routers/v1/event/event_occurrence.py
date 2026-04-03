from application.event.use_cases.crud.event_occurrence import EventOccurrenceCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class EventOccurrenceRouter(V1CrudRouter[EventOccurrenceCrudUseCase]):
    prefix = "/event-occurrences"
    tags = ["v1/event"]
    use_case_cls = EventOccurrenceCrudUseCase


event_occurrence_crud_router = EventOccurrenceRouter()
router = event_occurrence_crud_router.router

