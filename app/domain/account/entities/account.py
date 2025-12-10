from dataclasses import dataclass, field
from core.config.settings import settings
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin
from domain.base.mixins.with_active import WithActiveMixin


@dataclass(slots=True, kw_only=True)
class AccountEntity(BaseEntity, TimestampMixin, WithActiveMixin):
    """
    Domain entity representing a user account.

    Inherits:
        BaseEntity      - core entity base (id, immutability safeguards)
        TimestampMixin - created_at / updated_at timestamps
        WithActiveMixin - active/deactivated state

    Notes:
        Pure domain model. No ORM, no DTO, no infrastructure dependencies.
    """

    # ---------------------------
    # Required fields
    # ---------------------------
    username: str
    public_name: str | None

    # ---------------------------
    # Optional / computed fields
    # ---------------------------
    email: str | None = field(default=None, repr=False)
    language: str = settings.system.default_language
    is_online: bool = False
    avatar: str | None = None
    avatar_small: str | None = None
    avatar_medium: str | None = None
    avatar_large: str | None = None

    # ---------------------------
    # Domain behaviour
    # ---------------------------

    def get_email(self) -> str:
        """
        Return email if explicitly set, otherwise generate fallback email
        using a configured system email domain.
        """
        if self.email:
            return self.email
        return f"{self.username}@{settings.system.email_domain}"

    def get_display_name(self) -> str:
        """
        Return a name suitable for UI: public_name if available,
        otherwise fallback to username.
        """
        return self.public_name or self.username

    @classmethod
    async def create_from_auth_provider_data(cls, auth_provider_data: BaseAuthProviderData) -> "AccountEntity":
        return cls(
            username=auth_provider_data.get_username(),
            language=auth_provider_data.get_language_code() or settings.system.default_language,
            public_name=auth_provider_data.get_public_name(),
            avatar=await auth_provider_data.get_image_url()
        )
