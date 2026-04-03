from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.discussion.entities.discussion_attachment import DiscussionAttachmentEntity
from domain.discussion.repositories.discussion import DiscussionAttachmentFilter


class DiscussionAttachmentCrudUseCase(BaseCrudUseCase[DiscussionAttachmentEntity, DiscussionAttachmentFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(DiscussionAttachmentEntity, DiscussionAttachmentFilter, account=account)

