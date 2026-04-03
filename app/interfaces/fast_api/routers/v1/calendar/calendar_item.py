from application.calendar.use_cases.crud.calendar_item import CalendarItemCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class CalendarItemRouter(V1CrudRouter[CalendarItemCrudUseCase]):
    prefix = "/calendar-items"
    tags = ["v1/calendar"]
    use_case_cls = CalendarItemCrudUseCase


calendar_item_crud_router = CalendarItemRouter()
router = calendar_item_crud_router.router

