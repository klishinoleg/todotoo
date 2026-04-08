from __future__ import annotations

from application.account.dto.account import AccountDTO
from application.account.dto.profile import ProfileUpdateRequestDTO
from application.account.services.account import AccountService
from application.account.services.avatar_storage import AvatarStorageService
from core.i18n import get_supported_languages
from core.enums.system.error_fields import ErrorFields
from core.messages.account.access_control import AccessControlMessages
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException


class ProfileUseCase:
    def __init__(self) -> None:
        self.account_service = AccountService()
        self.avatar_storage_service = AvatarStorageService()

    async def get_profile(self, account: AccountEntity) -> AccountDTO:
        entity = await self._get_account_or_raise(account)
        return AccountDTO.from_entity(entity)

    async def update_profile(self, account: AccountEntity, dto: ProfileUpdateRequestDTO) -> AccountDTO:
        entity = await self._get_account_or_raise(account)
        updates: dict[str, str | None] = {}

        if dto.public_name is not None:
            public_name = dto.public_name.strip()
            updates["public_name"] = public_name or None

        if dto.language is not None:
            language = dto.language.strip().lower()
            if language not in set(get_supported_languages()):
                raise DomainValidationException(
                    message=AccessControlMessages.invalid_profile_language(language),
                    field=ErrorFields.ACCOUNT,
                )
            updates["language"] = language

        if not updates:
            return AccountDTO.from_entity(entity)

        saved = await self.account_service.save(entity.get_new_updated(updates), update_fields=set(updates.keys()))
        return AccountDTO.from_entity(saved)

    async def upload_avatar(
            self, account: AccountEntity, *, filename: str | None, content_type: str | None, content: bytes
    ) -> AccountDTO:
        entity = await self._get_account_or_raise(account)
        key = await self.avatar_storage_service.persist_uploaded_avatar(
            filename=filename,
            content_type=content_type,
            content=content,
        )
        if not key:
            raise DomainValidationException(
                message=AccessControlMessages.invalid_avatar_file(),
                field=ErrorFields.ACCOUNT,
            )
        saved = await self.account_service.save(entity.get_new_updated({"avatar": key}), update_fields={"avatar"})
        return AccountDTO.from_entity(saved)

    async def delete_avatar(self, account: AccountEntity) -> AccountDTO:
        entity = await self._get_account_or_raise(account)
        saved = await self.account_service.save(entity.get_new_updated({"avatar": None}), update_fields={"avatar"})
        return AccountDTO.from_entity(saved)

    async def _get_account_or_raise(self, account: AccountEntity) -> AccountEntity:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        found = await self.account_service.get(account.id)
        if found is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(account.id),
                field=ErrorFields.ACCOUNT,
            )
        return found
