from application.discussion.use_cases.crud.discussion_message import DiscussionMessageCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class DiscussionMessageRouter(V1CrudRouter[DiscussionMessageCrudUseCase]):
    prefix = "/discussion-messages"
    tags = ["v1/discussion"]
    use_case_cls = DiscussionMessageCrudUseCase


discussion_message_crud_router = DiscussionMessageRouter()
router = discussion_message_crud_router.router

