from dataclasses import dataclass, replace, asdict
from typing import Self

from core.di.access_control import DIPasswordHasherProvider
from core.di.auth import DIAuthProviderData
from core.enums.app.account.auth_provider import AuthProviderType
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from infrastructure.auth.providers.registration.registration_types import RegistrationInitData


@dataclass(slots=True)
class RegistrationProviderData(BaseAuthProviderData):
    """
    Domain-level provider data for email/password registration.
    """

    _data: RegistrationInitData
    provider_id_type = str

    def __init__(self, provider_raw_data: dict) -> None:
        super().__init__(provider_raw_data)
        self._data = RegistrationInitData(**provider_raw_data)

    def get_user_id(self) -> str:
        return self._data.email

    def get_username(self) -> str:
        return self._data.email

    def get_public_name(self) -> str | None:
        return self._data.public_name or self._data.email.split("@")[0]

    def get_is_premium(self) -> bool:
        return False

    def get_language_code(self) -> str | None:
        return self._data.language_code

    async def get_image_url(self) -> str | None:
        return None

    def get_contact_url(self) -> str | None:
        return f"mailto:{self._data.email}"

    def is_valid(self) -> bool:
        if not self._data.password:
            return False
        if self._data.confirm_password is None:
            return True
        return self._data.password == self._data.confirm_password

    def prepare_for_storage(self) -> Self:
        if self._data.password:
            _data = replace(self._data,
                            password_hash=DIPasswordHasherProvider.get().hash(self._data.password),
                            password="",
                            confirm_password=""
                            )
            return replace(self, _data=_data, _provider_raw_data=asdict(_data))
        return self

DIAuthProviderData.register(AuthProviderType.PASSWORD, RegistrationProviderData)
