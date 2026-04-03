from application.idea_event.use_cases.crud.event_comment import IdeaEventCommentCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaEventCommentRouter(V1CrudRouter[IdeaEventCommentCrudUseCase]):
    prefix = "/idea-event-comments"
    tags = ["v1/idea_event"]
    use_case_cls = IdeaEventCommentCrudUseCase


idea_event_comment_crud_router = IdeaEventCommentRouter()
router = idea_event_comment_crud_router.router

