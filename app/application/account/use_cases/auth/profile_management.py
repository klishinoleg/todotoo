from __future__ import annotations

from typing import Any
from uuid import uuid4

from application.account.dto.account_auth_profile import AccountAuthProfileDTO
from application.account.dto.auth.profile_management import AuthProfileLinkResponseDTO, AuthProfileDeleteResponseDTO
from application.account.services.account import AccountService
from application.account.services.account_auth_profile import AccountAuthProfileService
from core.config.settings import settings
from core.di.auth import DIAuthProviderData
from core.di.repository import DIRepositoryTransaction
from core.enums.app.account.auth_provider import AuthProviderType
from core.enums.system.error_fields import ErrorFields
from core.enums.system.logger.message_levels import LogMessageLevel
from core.fast_storage import get_fast_storage
from core.logger.logger import Logger
from core.messages.account.access_control import AccessControlMessages
from domain.account.entities.account import AccountEntity
from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.base.exceptions import DomainValidationException


class AuthProfileManagementUseCase:
    def __init__(self) -> None:
        self.account_service = AccountService()
        self.account_auth_profile_service = AccountAuthProfileService()
        self.repository_transaction = DIRepositoryTransaction.get()

    async def list_profiles(self, account: AccountEntity) -> list[AccountAuthProfileDTO]:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        profiles = await self.account_auth_profile_service.get_by_account_id(account.id)
        Logger.auth(
            "auth.profile.list",
            account_id=account.id,
            count=len(profiles),
        )
        return [AccountAuthProfileDTO.from_entity(item) for item in profiles]

    async def link_profile(
            self,
            account: AccountEntity,
            provider_type: AuthProviderType,
            provider_raw_data: dict[str, Any],
            confirm_merge: bool = False,
            force_merge: bool = False,
    ) -> AuthProfileLinkResponseDTO:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        Logger.auth(
            "auth.profile.link.start",
            account_id=account.id,
            provider_type=str(provider_type),
            confirm_merge=confirm_merge,
        )

        provider_data = DIAuthProviderData.get(provider_type, provider_raw_data)
        await self.account_auth_profile_service.ensure_is_valid_provider_data(provider_type, provider_data)

        current_profiles = await self.account_auth_profile_service.get_by_account_id(account.id)
        if any(p.provider_type == provider_type for p in current_profiles):
            Logger.auth(
                "auth.profile.link.duplicate_provider",
                level=LogMessageLevel.WARN,
                account_id=account.id,
                provider_type=str(provider_type),
            )
            raise DomainValidationException(
                message=AccessControlMessages.auth_provider_already_linked(provider_type),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        existed_profile = await self.account_auth_profile_service.get_or_none_by_provider_and_id(provider_type, provider_data)
        if existed_profile:
            if existed_profile.account_id == account.id:
                Logger.auth(
                    "auth.profile.link.already_linked",
                    account_id=account.id,
                    provider_type=str(provider_type),
                    profile_id=existed_profile.id,
                )
                return AuthProfileLinkResponseDTO(
                    status="already_linked",
                    profile=AccountAuthProfileDTO.from_entity(existed_profile),
                )
            if not force_merge:
                Logger.auth(
                    "auth.profile.link.merge_required",
                    level=LogMessageLevel.WARN,
                    account_id=account.id,
                    provider_type=str(provider_type),
                    conflict_account_id=existed_profile.account_id,
                    conflict_profile_id=existed_profile.id,
                )
                operation_code = await self._create_merge_operation(
                    account_id=account.id,
                    provider_type=provider_type,
                    provider_raw_data=provider_raw_data,
                    conflict_account_id=existed_profile.account_id,
                )
                return AuthProfileLinkResponseDTO(
                    status="confirmation_required",
                    detail=AccessControlMessages.auth_profile_merge_confirmation_required(existed_profile.account_id),
                    operation_code=operation_code,
                )

            async with self.repository_transaction.start():
                deleted_conflict_account = await self.account_service.delete(existed_profile.account_id)
                if not deleted_conflict_account:
                    Logger.auth(
                        "auth.profile.link.merge_account_delete_failed",
                        level=LogMessageLevel.WARN,
                        account_id=account.id,
                        provider_type=str(provider_type),
                        conflict_account_id=existed_profile.account_id,
                    )
                    raise DomainValidationException(
                        message=AccessControlMessages.account_not_found(existed_profile.account_id),
                        field=ErrorFields.ACCOUNT,
                    )
                new_profile = AccountAuthProfileEntity.create_from_provider_type_and_data(
                    provider_type=provider_type,
                    account_id=account.id,
                    provider_data=provider_data.prepare_for_storage(),
                )
                created_profile = await self.account_auth_profile_service.create(new_profile)
            Logger.auth(
                "auth.profile.link.merged",
                account_id=account.id,
                provider_type=str(provider_type),
                conflict_account_id=existed_profile.account_id,
                profile_id=created_profile.id,
            )
            return AuthProfileLinkResponseDTO(
                status="linked",
                profile=AccountAuthProfileDTO.from_entity(created_profile),
                merged_account_id=existed_profile.account_id,
                merged_account_deleted=True,
            )

        new_profile = AccountAuthProfileEntity.create_from_provider_type_and_data(
            provider_type=provider_type,
            account_id=account.id,
            provider_data=provider_data.prepare_for_storage(),
        )
        created_profile = await self.account_auth_profile_service.create(new_profile)
        Logger.auth(
            "auth.profile.link.created",
            account_id=account.id,
            provider_type=str(provider_type),
            profile_id=created_profile.id,
        )
        return AuthProfileLinkResponseDTO(
            status="linked",
            profile=AccountAuthProfileDTO.from_entity(created_profile),
        )

    async def delete_profile(self, account: AccountEntity, profile_id: int) -> AuthProfileDeleteResponseDTO:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        Logger.auth(
            "auth.profile.delete.start",
            account_id=account.id,
            profile_id=profile_id,
        )
        profile = await self.account_auth_profile_service.get(profile_id)
        if profile is None:
            Logger.auth(
                "auth.profile.delete.not_found",
                level=LogMessageLevel.WARN,
                account_id=account.id,
                profile_id=profile_id,
            )
            raise DomainValidationException(
                message=AccessControlMessages.account_auth_profile_not_found(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        if profile.account_id != account.id:
            Logger.auth(
                "auth.profile.delete.forbidden",
                level=LogMessageLevel.WARN,
                account_id=account.id,
                profile_id=profile_id,
                profile_account_id=profile.account_id,
            )
            raise DomainValidationException(
                message=AccessControlMessages.auth_profile_does_not_belong_to_account(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        all_profiles = await self.account_auth_profile_service.get_by_account_id(account.id)
        if len(all_profiles) <= 1:
            Logger.auth(
                "auth.profile.delete.last_profile_blocked",
                level=LogMessageLevel.WARN,
                account_id=account.id,
                profile_id=profile_id,
            )
            raise DomainValidationException(
                message=AccessControlMessages.cannot_delete_last_auth_profile(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        deleted = await self.account_auth_profile_service.delete(profile_id)
        if not deleted:
            raise DomainValidationException(
                message=AccessControlMessages.account_auth_profile_not_found(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )
        Logger.auth(
            "auth.profile.delete.success",
            account_id=account.id,
            profile_id=profile_id,
        )
        return AuthProfileDeleteResponseDTO(status="deleted", profile_id=profile_id)

    async def confirm_link_merge(self, account: AccountEntity, operation_code: str) -> AuthProfileLinkResponseDTO:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        Logger.auth(
            "auth.profile.link.confirm.start",
            account_id=account.id,
            operation_code=operation_code,
        )
        operation = await self._get_merge_operation(operation_code)
        if operation is None:
            Logger.auth(
                "auth.profile.link.confirm.operation_not_found",
                level=LogMessageLevel.WARN,
                account_id=account.id,
                operation_code=operation_code,
            )
            raise DomainValidationException(
                message=AccessControlMessages.auth_profile_merge_operation_not_found(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        op_account_id = int(operation.get("account_id") or 0)
        if op_account_id != account.id:
            Logger.auth(
                "auth.profile.link.confirm.forbidden",
                level=LogMessageLevel.WARN,
                account_id=account.id,
                operation_code=operation_code,
                operation_account_id=op_account_id,
            )
            raise DomainValidationException(
                message=AccessControlMessages.auth_profile_merge_operation_forbidden(),
                field=ErrorFields.AUTH_PROVIDER_DATA,
            )

        provider_type = AuthProviderType(str(operation["provider_type"]))
        provider_raw_data = operation["provider_raw_data"]
        result = await self.link_profile(
            account=account,
            provider_type=provider_type,
            provider_raw_data=provider_raw_data,
            confirm_merge=True,
            force_merge=True,
        )
        await self._delete_merge_operation(operation_code)
        Logger.auth(
            "auth.profile.link.confirm.success",
            account_id=account.id,
            operation_code=operation_code,
            status=result.status,
            profile_id=result.profile.id if result.profile else None,
        )
        return result

    async def _create_merge_operation(
            self,
            account_id: int,
            provider_type: AuthProviderType,
            provider_raw_data: dict[str, Any],
            conflict_account_id: int,
    ) -> str:
        operation_code = uuid4().hex
        payload = {
            "account_id": account_id,
            "provider_type": str(provider_type),
            "provider_raw_data": provider_raw_data,
            "conflict_account_id": conflict_account_id,
        }
        storage = get_fast_storage()
        await storage.set_json(
            key=self._operation_key(operation_code),
            value=payload,
            ttl_seconds=settings.fast_storage.operation_ttl_seconds,
        )
        Logger.auth(
            "auth.profile.link.operation.created",
            account_id=account_id,
            provider_type=str(provider_type),
            conflict_account_id=conflict_account_id,
            operation_code=operation_code,
        )
        return operation_code

    async def _get_merge_operation(self, operation_code: str) -> dict[str, Any] | None:
        storage = get_fast_storage()
        return await storage.get_json(self._operation_key(operation_code))

    async def _delete_merge_operation(self, operation_code: str) -> None:
        storage = get_fast_storage()
        await storage.delete(self._operation_key(operation_code))

    @staticmethod
    def _operation_key(operation_code: str) -> str:
        return f"auth:profile:merge:{operation_code}"
