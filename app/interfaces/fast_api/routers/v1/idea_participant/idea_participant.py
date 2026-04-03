from application.idea_participant.use_cases.crud.idea_participant import IdeaParticipantCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaParticipantRouter(V1CrudRouter[IdeaParticipantCrudUseCase]):
    prefix = "/idea-participants"
    tags = ["v1/idea_participant"]
    use_case_cls = IdeaParticipantCrudUseCase


idea_participant_crud_router = IdeaParticipantRouter()
router = idea_participant_crud_router.router

