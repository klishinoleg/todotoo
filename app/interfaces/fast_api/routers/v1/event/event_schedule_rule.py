from application.event.use_cases.crud.event_schedule_rule import EventScheduleRuleCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class EventScheduleRuleRouter(V1CrudRouter[EventScheduleRuleCrudUseCase]):
    prefix = "/event-schedule-rules"
    tags = ["v1/event"]
    use_case_cls = EventScheduleRuleCrudUseCase


event_schedule_rule_crud_router = EventScheduleRuleRouter()
router = event_schedule_rule_crud_router.router

