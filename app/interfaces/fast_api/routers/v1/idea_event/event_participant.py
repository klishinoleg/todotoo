from application.idea_event.use_cases.crud.event_participant import IdeaEventParticipantCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaEventParticipantRouter(V1CrudRouter[IdeaEventParticipantCrudUseCase]):
    prefix = "/idea-event-participants"
    tags = ["v1/idea_event"]
    use_case_cls = IdeaEventParticipantCrudUseCase


idea_event_participant_crud_router = IdeaEventParticipantRouter()
router = idea_event_participant_crud_router.router

