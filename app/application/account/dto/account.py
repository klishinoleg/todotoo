from application.base.dto.base import ItemDTO, ListDTO


class AccountDTO(ItemDTO):
    """
    Full representation of AccountEntity for external interfaces.
    Mirrors detailed entity fields suitable for UI.
    """
    username: str
    public_name: str | None
    email: str | None
    language: str
    is_online: bool
    avatar: str | None
    avatar_small: str | None
    avatar_medium: str | None
    avatar_large: str | None


class AccountListDTO(ListDTO):
    """
    Lightweight version of AccountDTO for list views.
    Only fields required by listings are included.
    """
    username: str
    public_name: str | None
    avatar_small: str | None
