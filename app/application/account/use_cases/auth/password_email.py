from __future__ import annotations

import secrets
import string
from uuid import uuid4

from application.account.dto.account_auth_profile import AccountAuthProfileDTO
from application.account.dto.auth.password_email import (
    AuthChangePasswordRequestDTO,
    AuthMailPasswordResponseDTO,
    AuthRecoverPasswordRequestDTO,
    AuthRegisterByEmailRequestDTO,
    AuthResetPasswordByCodeRequestDTO,
    AuthSetPasswordRequestDTO,
    AuthSetPasswordResponseDTO,
)
from application.account.services.account import AccountService
from application.account.services.account_auth_profile import AccountAuthProfileService
from core.di.access_control import DIPasswordHasherProvider
from core.di.auth import DIAuthProviderData
from core.di.repository import DIRepositoryTransaction
from core.config.settings import settings
from core.email import get_email_sender
from core.fast_storage import get_fast_storage
from core.enums.app.account.auth_provider import AuthProviderType
from core.enums.system.error_fields import ErrorFields
from core.messages.account.access_control import AccessControlMessages
from domain.account.entities.account import AccountEntity
from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from domain.base.exceptions import DomainValidationException


class PasswordEmailAuthUseCase:
    def __init__(self) -> None:
        self.account_service = AccountService()
        self.account_auth_profile_service = AccountAuthProfileService()
        self.repository_transaction = DIRepositoryTransaction.get()

    async def register_by_email(self, dto: AuthRegisterByEmailRequestDTO) -> AuthMailPasswordResponseDTO:
        email = dto.email.strip().lower()
        if not email:
            raise DomainValidationException(
                message=AccessControlMessages.password_profile_required(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        existed_account = await self.account_service.get_by_username_or_email(email)
        existed_profile = await self._get_password_profile_by_email(email)
        if existed_account is not None or existed_profile is not None:
            raise DomainValidationException(
                message=AccessControlMessages.email_already_registered(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        password = self._generate_password()
        await self._create_account_with_password_profile(
            email=email,
            password=password,
            public_name=dto.public_name,
            language_code=dto.language_code,
        )

        await self._send_password_email(email, password, subject="Your login password")
        return AuthMailPasswordResponseDTO(status="sent", email=email)

    async def recover_password(self, dto: AuthRecoverPasswordRequestDTO) -> AuthMailPasswordResponseDTO:
        email = dto.email.strip().lower()
        profile = await self._get_password_profile_by_email(email)
        if profile is None:
            raise DomainValidationException(
                message=AccessControlMessages.password_profile_required(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        code = await self._create_password_recovery_code(email)
        link = self._build_recovery_link(code)
        await self._send_recovery_email(email, link)
        return AuthMailPasswordResponseDTO(status="sent", email=email)

    async def reset_password_by_code(self, dto: AuthResetPasswordByCodeRequestDTO) -> AuthMailPasswordResponseDTO:
        if dto.password != dto.confirm_password:
            raise DomainValidationException(
                message=AccessControlMessages.invalid_auth_provider_data(AuthProviderType.PASSWORD),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        email = await self._consume_password_recovery_code(dto.code)
        if not email:
            raise DomainValidationException(
                message=AccessControlMessages.password_recovery_code_invalid_or_expired(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        profile = await self._get_password_profile_by_email(email)
        if profile is None:
            raise DomainValidationException(
                message=AccessControlMessages.password_profile_required(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        await self._set_profile_password(profile, dto.password)
        return AuthMailPasswordResponseDTO(status="reset", email=email)

    async def set_password_if_missing(
            self, account: AccountEntity, dto: AuthSetPasswordRequestDTO
    ) -> AuthSetPasswordResponseDTO:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        if dto.password != dto.confirm_password:
            raise DomainValidationException(
                message=AccessControlMessages.invalid_auth_provider_data(AuthProviderType.PASSWORD),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        profiles = await self.account_auth_profile_service.get_by_account_id(account.id)
        password_profile = next((p for p in profiles if p.provider_type == AuthProviderType.PASSWORD), None)
        if password_profile is not None:
            raw = password_profile.provider_data.serialize()
            if raw.get("password_hash"):
                raise DomainValidationException(
                    message=AccessControlMessages.password_already_set(),
                    field=ErrorFields.AUTH_PROVIDER_DATA,
                )
            updated = await self._set_profile_password(password_profile, dto.password)
            return AuthSetPasswordResponseDTO(status="set", profile=AccountAuthProfileDTO.from_entity(updated))

        email = (account.email or account.username or "").strip().lower()
        if not email:
            raise DomainValidationException(
                message=AccessControlMessages.password_profile_required(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        created = await self._create_password_profile_for_account(
            account=account,
            email=email,
            password=dto.password,
            public_name=account.public_name,
            language_code=account.language,
        )
        return AuthSetPasswordResponseDTO(status="set", profile=AccountAuthProfileDTO.from_entity(created))

    async def change_password(
            self, account: AccountEntity, dto: AuthChangePasswordRequestDTO
    ) -> AuthSetPasswordResponseDTO:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        if dto.password != dto.confirm_password:
            raise DomainValidationException(
                message=AccessControlMessages.invalid_auth_provider_data(AuthProviderType.PASSWORD),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        profiles = await self.account_auth_profile_service.get_by_account_id(account.id)
        password_profile = next((p for p in profiles if p.provider_type == AuthProviderType.PASSWORD), None)
        if password_profile is None:
            raise DomainValidationException(
                message=AccessControlMessages.password_profile_required(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        raw = password_profile.provider_data.serialize()
        stored_hash = raw.get("password_hash")
        if not stored_hash or not DIPasswordHasherProvider.get().verify(dto.current_password, str(stored_hash)):
            raise DomainValidationException(
                message=AccessControlMessages.invalid_username_or_password(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        updated = await self._set_profile_password(password_profile, dto.password)
        return AuthSetPasswordResponseDTO(status="changed", profile=AccountAuthProfileDTO.from_entity(updated))

    async def _create_account_with_password_profile(
            self, *, email: str, password: str, public_name: str | None, language_code: str | None
    ) -> tuple[AccountEntity, AccountAuthProfileEntity]:
        provider_data = self._build_registration_provider_data(
            email=email,
            password=password,
            public_name=public_name,
            language_code=language_code,
        ).prepare_for_storage()
        async with self.repository_transaction.start():
            new_account = await AccountEntity.create_from_auth_provider_data(provider_data)
            account = await self.account_service.create(new_account)
            assert account.id is not None
            auth_profile = AccountAuthProfileEntity.create_from_provider_type_and_data(
                provider_type=AuthProviderType.PASSWORD,
                account_id=account.id,
                provider_data=provider_data,
            )
            profile = await self.account_auth_profile_service.create(auth_profile)
        return account, profile

    async def _create_password_profile_for_account(
            self,
            *,
            account: AccountEntity,
            email: str,
            password: str,
            public_name: str | None,
            language_code: str | None,
    ) -> AccountAuthProfileEntity:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        provider_data = self._build_registration_provider_data(
            email=email,
            password=password,
            public_name=public_name,
            language_code=language_code,
        ).prepare_for_storage()
        new_profile = AccountAuthProfileEntity.create_from_provider_type_and_data(
            provider_type=AuthProviderType.PASSWORD,
            account_id=account.id,
            provider_data=provider_data,
        )
        return await self.account_auth_profile_service.create(new_profile)

    async def _set_profile_password(
            self, profile: AccountAuthProfileEntity, password: str
    ) -> AccountAuthProfileEntity:
        raw = profile.provider_data.serialize()
        provider_data = self._build_registration_provider_data(
            email=str(raw.get("email") or profile.provider_id),
            password=password,
            public_name=raw.get("public_name"),
            language_code=raw.get("language_code"),
        ).prepare_for_storage()
        updated = profile.get_new_updated(
            {
                "provider_data": provider_data,
                "provider_id": str(provider_data.get_user_id()),
                "language_code": provider_data.get_language_code(),
            }
        )
        return await self.account_auth_profile_service.save(
            updated, update_fields={"provider_data", "provider_id", "language_code"}
        )

    async def _get_password_profile_by_email(self, email: str) -> AccountAuthProfileEntity | None:
        provider_data = self._build_registration_provider_data(
            email=email, password="dummy-password", public_name=None, language_code=None
        )
        return await self.account_auth_profile_service.get_or_none_by_provider_and_id(
            AuthProviderType.PASSWORD,
            provider_data,
        )

    @staticmethod
    def _build_registration_provider_data(
            *, email: str, password: str, public_name: str | None, language_code: str | None
    ) -> BaseAuthProviderData:
        return DIAuthProviderData.get(
            AuthProviderType.PASSWORD,
            {
                "email": email,
                "password": password,
                "confirm_password": password,
                "public_name": public_name,
                "language_code": language_code,
                "ip": None,
                "user_agent": None,
                "start_param": None,
            },
        )

    @staticmethod
    def _generate_password(length: int = 12) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def _generate_recovery_code() -> str:
        return uuid4().hex

    @staticmethod
    async def _send_password_email(email: str, password: str, *, subject: str) -> None:
        sender = get_email_sender()
        text = (
            f"Hello,\n\nYour password: {password}\n\n"
            "Use it to login and change it later.\n"
        )
        await sender.send_email(to_email=email, subject=subject, text_body=text)

    async def _create_password_recovery_code(self, email: str) -> str:
        code = self._generate_recovery_code()
        storage = get_fast_storage()
        await storage.set_json(
            key=self._recovery_key(code),
            value={"email": email},
            ttl_seconds=settings.email.password_recovery_ttl_seconds,
        )
        return code

    async def _consume_password_recovery_code(self, code: str) -> str | None:
        storage = get_fast_storage()
        payload = await storage.get_json(self._recovery_key(code))
        await storage.delete(self._recovery_key(code))
        if not payload:
            return None
        email = str(payload.get("email") or "").strip().lower()
        return email or None

    @staticmethod
    def _recovery_key(code: str) -> str:
        return f"auth:password:recovery:{code}"

    @staticmethod
    def _build_recovery_link(code: str) -> str:
        base_url = settings.email.password_recovery_page_url.strip()
        if not base_url:
            web_app = settings.system.web_app_url.strip().rstrip("/")
            base_url = f"{web_app}/auth/password-recovery"
        separator = "&" if "?" in base_url else "?"
        return f"{base_url}{separator}code={code}"

    @staticmethod
    async def _send_recovery_email(email: str, recovery_link: str) -> None:
        sender = get_email_sender()
        text = (
            "Hello,\n\n"
            "Use this link to reset your password:\n"
            f"{recovery_link}\n\n"
            "If you did not request a reset, ignore this email.\n"
        )
        await sender.send_email(to_email=email, subject="Password recovery", text_body=text)
