from application.meeting.use_cases.crud.meeting_participant import MeetingParticipantCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class MeetingParticipantRouter(V1CrudRouter[MeetingParticipantCrudUseCase]):
    prefix = "/meeting-participants"
    tags = ["v1/meeting"]
    use_case_cls = MeetingParticipantCrudUseCase


meeting_participant_crud_router = MeetingParticipantRouter()
router = meeting_participant_crud_router.router

