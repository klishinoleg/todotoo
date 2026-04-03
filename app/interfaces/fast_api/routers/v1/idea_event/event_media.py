from application.idea_event.use_cases.crud.event_media import IdeaEventMediaCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaEventMediaRouter(V1CrudRouter[IdeaEventMediaCrudUseCase]):
    prefix = "/idea-event-media"
    tags = ["v1/idea_event"]
    use_case_cls = IdeaEventMediaCrudUseCase


idea_event_media_crud_router = IdeaEventMediaRouter()
router = idea_event_media_crud_router.router

