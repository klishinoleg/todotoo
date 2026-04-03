from dataclasses import dataclass

from core.enums.app.idea.status import IdeaStatusEnum
from core.enums.app.idea.visibility import IdeaVisibilityEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin
from domain.base.mixins.with_active import WithActiveMixin


@dataclass(slots=True, kw_only=True)
class IdeaEntity(BaseEntity, WithActiveMixin, TimestampMixin):
    title: str
    description: str
    slogan: str | None = None
    cover_image: str | None = None
    creator_id: int
    visibility: IdeaVisibilityEnum = IdeaVisibilityEnum.PUBLIC
    status: IdeaStatusEnum = IdeaStatusEnum.DRAFT

