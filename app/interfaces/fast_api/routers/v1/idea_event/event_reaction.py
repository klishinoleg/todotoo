from application.idea_event.use_cases.crud.event_reaction import IdeaEventReactionCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaEventReactionRouter(V1CrudRouter[IdeaEventReactionCrudUseCase]):
    prefix = "/idea-event-reactions"
    tags = ["v1/idea_event"]
    use_case_cls = IdeaEventReactionCrudUseCase


idea_event_reaction_crud_router = IdeaEventReactionRouter()
router = idea_event_reaction_crud_router.router

