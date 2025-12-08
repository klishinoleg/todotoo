from application.base.dto.base import ItemDTO, ListDTO


class TagDTO(ItemDTO):
    """
    Full representation of the Tag entity for external interfaces.
    Mirrors detailed tag fields suitable for UI.
    """
    name: str
    slug: str
    parent_id: int | None
    ordering: int
    is_active: bool
    icon: str | None
    icon_small: str | None
    icon_middle: str | None


class TagListDTO(ListDTO):
    """
    Lightweight version of TagDTO for list views.
    Only fields required by listings are included.
    """
    name: str
    slug: str
    parent_id: int | None
    is_active: bool
    icon_small: str | None
