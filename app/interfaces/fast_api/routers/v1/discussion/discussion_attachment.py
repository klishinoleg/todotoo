from application.discussion.use_cases.crud.discussion_attachment import DiscussionAttachmentCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class DiscussionAttachmentRouter(V1CrudRouter[DiscussionAttachmentCrudUseCase]):
    prefix = "/discussion-attachments"
    tags = ["v1/discussion"]
    use_case_cls = DiscussionAttachmentCrudUseCase


discussion_attachment_crud_router = DiscussionAttachmentRouter()
router = discussion_attachment_crud_router.router

