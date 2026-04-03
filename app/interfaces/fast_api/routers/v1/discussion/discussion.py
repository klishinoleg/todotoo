from application.discussion.use_cases.crud.discussion import DiscussionCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class DiscussionRouter(V1CrudRouter[DiscussionCrudUseCase]):
    prefix = "/discussions"
    tags = ["v1/discussion"]
    use_case_cls = DiscussionCrudUseCase


discussion_crud_router = DiscussionRouter()
router = discussion_crud_router.router

