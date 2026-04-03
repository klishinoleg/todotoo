from abc import ABC

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.string_filters import TextFilterField
from domain.base.repository import BaseRepository
from domain.discussion.entities.discussion import DiscussionEntity
from domain.discussion.entities.discussion_attachment import DiscussionAttachmentEntity
from domain.discussion.entities.discussion_message import DiscussionMessageEntity


class DiscussionFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    created_by: EqualFilterField[int, Q] | None = None
    title: TextFilterField[Q] | None = None


class DiscussionRepository[Q](BaseRepository[DiscussionEntity, DiscussionFilter[Q]], ABC):
    ...


class DiscussionMessageFilter[Q](BaseFilter[Q]):
    discussion_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    text: TextFilterField[Q] | None = None


class DiscussionMessageRepository[Q](BaseRepository[DiscussionMessageEntity, DiscussionMessageFilter[Q]], ABC):
    ...


class DiscussionAttachmentFilter[Q](BaseFilter[Q]):
    message_id: EqualFilterField[int, Q] | None = None
    file_type: EqualFilterField[str, Q] | None = None


class DiscussionAttachmentRepository[Q](BaseRepository[DiscussionAttachmentEntity, DiscussionAttachmentFilter[Q]], ABC):
    ...

