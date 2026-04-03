from application.meeting.use_cases.crud.meeting import MeetingCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class MeetingRouter(V1CrudRouter[MeetingCrudUseCase]):
    prefix = "/meetings"
    tags = ["v1/meeting"]
    use_case_cls = MeetingCrudUseCase


meeting_crud_router = MeetingRouter()
router = meeting_crud_router.router

