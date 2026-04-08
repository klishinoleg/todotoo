from application.account.dto.account import AccountDTO
from application.account.dto.account_auth_profile import AccountAuthProfileDTO
from application.account.dto.auth.request.oauth import AuthRequestOAuthDTO, AuthRequestOAuthLoginDTO, AuthRequestOAuthSignUpDTO
from application.account.dto.auth.request.registration import AuthRequestSignUpDTO, AuthRequestLoginDTO
from application.account.dto.auth.request.telegram import AuthRequestTelegramDTO
from application.account.dto.auth.response import AuthResponseDTO
from application.account.services.account import AccountService
from application.account.services.account_auth_profile import AccountAuthProfileService
from application.account.services.avatar_storage import AvatarStorageService
from application.account.services.account_session import AccountSessionService
from core.di.access_control import DIAccessTokenProvider, DIPasswordHasherProvider
from core.di.auth import DIAuthProviderData
from core.di.repository import DIRepositoryTransaction
from core.enums.app.account.auth_provider import AuthProviderType
from core.enums.system.error_fields import ErrorFields
from core.enums.system.logger.message_levels import LogMessageLevel
from core.exceptions.system import AccessControlException
from core.logger.logger import Logger
from core.messages.account.access_control import AccessControlMessages
from core.messages.system.no_localized_messages import SystemMessages
from core.storage import get_storage
from domain.account.entities.account import AccountEntity
from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from domain.base.exceptions import DomainValidationException


class AuthUseCase:
    """
    High-level authentication uses case orchestrator.

    Responsibilities:
    - Coordinate account creation / lookup and auth profile binding.
    - Work with different authentication providers via DIAuthProviderData.
    - Wrap all write operations in a repository transaction.
    - Produce API-ready DTOs with access tokens.
    """

    def __init__(self) -> None:
        self.account_service = AccountService()
        self.account_auth_profile_service = AccountAuthProfileService()
        self.repository_transaction = DIRepositoryTransaction.get()
        self.account_session_service = AccountSessionService()
        self.avatar_storage_service = AvatarStorageService()

    async def _create_account_with_auth_profile(
            self, provider_type: AuthProviderType, provider_data: BaseAuthProviderData
    ) -> tuple[AccountEntity, AccountAuthProfileEntity]:
        """
        Create a new account and bind a new auth profile for the given provider.

        Steps:
        1. Start a repository-level transaction.
        2. Normalize/prepare raw provider data for persistent storage.
        3. Build a new AccountEntity from provider data and persist it.
        4. Build a new AccountAuthProfileEntity linked to the created account and persist it.
        5. Commit the transaction and return both entities.

        Args:
            provider_type: Authentication provider type (e.g., TELEGRAM, PASSWORD).
            provider_data: Provider-specific data adapter used to extract normalized fields.

        Returns:
            Tuple of (an account, auth_profile) persisted in the repository.
        """
        async with self.repository_transaction.start():
            prepared_provider_data = provider_data.prepare_for_storage()
            new_account = await AccountEntity.create_from_auth_provider_data(prepared_provider_data)
            persisted_avatar = await self.avatar_storage_service.persist_external_avatar(new_account.avatar)
            if persisted_avatar != new_account.avatar:
                new_account = new_account.get_new_updated({"avatar": persisted_avatar})
            Logger.auth(
                "auth.oauth.account_create.attempt",
                provider_type=str(provider_type),
                username=str(getattr(new_account, "username", "")),
                email=str(getattr(new_account, "email", "")),
                public_name=str(getattr(new_account, "public_name", "")),
            )
            try:
                account = await self.account_service.create(new_account)
            except Exception as exc:
                Logger.auth(
                    "auth.oauth.account_create.error",
                    level=LogMessageLevel.WARN,
                    provider_type=str(provider_type),
                    detail=str(exc),
                )
                raise DomainValidationException(
                    message=f"Account creation failed: {exc}",
                    field=ErrorFields.ACCOUNT,
                )
            assert account.id is not None
            new_auth_profile = AccountAuthProfileEntity.create_from_provider_type_and_data(
                provider_type, account.id, prepared_provider_data)
            try:
                auth_profile = await self.account_auth_profile_service.create(new_auth_profile)
            except Exception as exc:
                Logger.auth(
                    "auth.oauth.profile_create.error",
                    level=LogMessageLevel.WARN,
                    provider_type=str(provider_type),
                    account_id=account.id,
                    detail=str(exc),
                )
                raise DomainValidationException(
                    message=f"Auth profile creation failed: {exc}",
                    field=ErrorFields.AUTH_PROVIDER_DATA,
                )
        return account, auth_profile

    async def _sync_account_avatar(self, account: AccountEntity, provider_data: BaseAuthProviderData) -> AccountEntity:
        # Keep user-selected/custom avatar untouched after first assignment.
        if account.avatar:
            return account

        provider_avatar = await provider_data.get_image_url()
        if not provider_avatar:
            return account

        persisted_avatar = await self.avatar_storage_service.persist_external_avatar(provider_avatar)
        if not persisted_avatar:
            return account

        storage = get_storage()
        current_key = storage.to_key(account.avatar)
        target_key = storage.to_key(persisted_avatar)
        if current_key and target_key and current_key == target_key:
            return account

        updated = account.get_new_updated({"avatar": persisted_avatar})
        saved = await self.account_service.save(updated, update_fields={"avatar"})
        Logger.auth(
            "auth.oauth.avatar.synced",
            account_id=saved.id,
            avatar=storage.get_url(saved.avatar),
        )
        return saved

    @staticmethod
    def _get_response_dto(account: AccountEntity, auth_profile: AccountAuthProfileEntity) -> AuthResponseDTO:
        """
        Build an AuthResponseDTO from domain entities.

        Wraps:
        - AccountEntity → AccountDTO
        - AccountAuthProfileEntity → AccountAuthProfileDTO
        - Access token issued for the account.

        Args:
            account: Persisted account entity.
            auth_profile: Persisted auth profile entity bound to the account.

        Returns:
            AuthResponseDTO ready to be returned from API handlers.
        """
        assert account.id is not None
        return AuthResponseDTO(
            account=AccountDTO.from_entity(account),
            auth=AccountAuthProfileDTO.from_entity(auth_profile),
            token=DIAccessTokenProvider.get().create_token(account.id)
        )

    async def telegram(self, dto: AuthRequestTelegramDTO) -> AuthResponseDTO:
        """
        Authenticate or register a user via Telegram provider.

        Flow:
        - Convert incoming raw DTO data into provider-specific adapter.
        - Validate provider data against business rules.
        - Try to find an existing auth profile for this provider and user.
          * If found → reuse the linked account.
          * If not found → create a new account + auth profile in a transaction.
        - Build and return AuthResponseDTO with a fresh access token.

        Args:
            dto: Telegram-specific auth request data.

        Returns:
            AuthResponseDTO with account, auth profile and access token.
        """
        provider_data = DIAuthProviderData.get(dto.provider_type, dto.provider_data.model_dump())
        await self.account_auth_profile_service.ensure_is_valid_provider_data(dto.provider_type, provider_data)
        existed_auth_profile = await self.account_auth_profile_service.get_or_none_by_provider_and_id(
            dto.provider_type, provider_data
        )
        if existed_auth_profile:
            account = await self.account_service.get(existed_auth_profile.account_id)
            auth_profile = existed_auth_profile
        else:
            account, auth_profile = await self._create_account_with_auth_profile(dto.provider_type, provider_data)
        assert account is not None
        return self._get_response_dto(account, auth_profile)

    async def register(self, dto: AuthRequestSignUpDTO | AuthRequestOAuthSignUpDTO) -> AuthResponseDTO:
        """
        Register a new account using an external auth provider.

        The method always creates a new account + auth profile pair and
        does not attempt to reuse existing profiles.

        Args:
            dto: Generic sign-up request with provider type and provider data.

        Returns:
            AuthResponseDTO with a newly created account, auth profile and token.
        """
        provider_data = DIAuthProviderData.get(dto.provider_type, dto.provider_data.model_dump())
        await self.account_auth_profile_service.ensure_is_valid_provider_data(dto.provider_type, provider_data)
        account, auth_profile = await self._create_account_with_auth_profile(dto.provider_type, provider_data)
        return self._get_response_dto(account, auth_profile)

    async def oauth_auth(self, dto: AuthRequestOAuthDTO) -> AuthResponseDTO:
        Logger.auth(
            "auth.oauth.auto.start",
            provider_type=str(dto.provider_type),
        )
        provider_data = DIAuthProviderData.get(dto.provider_type, dto.provider_data.model_dump())
        await self.account_auth_profile_service.ensure_is_valid_provider_data(dto.provider_type, provider_data)
        existed_auth_profile = await self.account_auth_profile_service.get_or_none_by_provider_and_id(
            dto.provider_type, provider_data
        )
        if existed_auth_profile:
            account = await self.account_service.get(existed_auth_profile.account_id)
            auth_profile = existed_auth_profile
            assert account is not None
            account = await self._sync_account_avatar(account, provider_data)
            Logger.auth(
                "auth.oauth.auto.login",
                provider_type=str(dto.provider_type),
                account_id=account.id if account else None,
                profile_id=auth_profile.id,
            )
        else:
            account, auth_profile = await self._create_account_with_auth_profile(dto.provider_type, provider_data)
            account = await self._sync_account_avatar(account, provider_data)
            Logger.auth(
                "auth.oauth.auto.register",
                provider_type=str(dto.provider_type),
                account_id=account.id,
                profile_id=auth_profile.id,
            )
        assert account is not None
        return self._get_response_dto(account, auth_profile)

    async def login(self, dto: AuthRequestLoginDTO | AuthRequestOAuthLoginDTO) -> AuthResponseDTO:
        """
        Log in an existing user using an external auth provider.

        Flow:
        - Resolve provider-specific adapter from incoming DTO.
        - Fetch existing auth profile by provider and provider user ID.
        - Load the linked account.
        - Build and return AuthResponseDTO with a fresh access token.

        Args:
            dto: Generic login request with provider type and provider data.

        Raises:
            AuthProviderException or domain-level exceptions if:
                - Provider data is invalid.
                - Auth profile for a given provider / user is not found.

        Returns:
            AuthResponseDTO with an existing account, auth profile and token.
        """
        provider_data = DIAuthProviderData.get(dto.provider_type, dto.provider_data.model_dump())
        auth_profile = await self.account_auth_profile_service.get_or_raise_by_provider_and_id(dto.provider_type,
                                                                                               provider_data)
        if dto.provider_type == AuthProviderType.PASSWORD:
            password = str(getattr(dto.provider_data, "password", ""))
            stored_hash = auth_profile.provider_data.serialize().get("password_hash")
            if not stored_hash or not DIPasswordHasherProvider.get().verify(password, str(stored_hash)):
                raise DomainValidationException(
                    message=AccessControlMessages.invalid_username_or_password(),
                    field=ErrorFields.AUTH_PROVIDER_DATA,
                )
        account = await self.account_service.get(auth_profile.account_id)
        assert account is not None
        return self._get_response_dto(account, auth_profile)

    @staticmethod
    async def me(account: AccountEntity) -> AccountDTO:
        return AccountDTO.from_entity(account)

    async def profiles(self, account: AccountEntity) -> list[AccountAuthProfileDTO]:
        assert account.id is not None
        profiles = await self.account_auth_profile_service.get_by_account_id(account.id)
        return list(map(AccountAuthProfileDTO.from_entity, profiles))

    async def logout(self, account: AccountEntity) -> bool:
        if account.id is None:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT,
            )
        return await self.account_session_service.close_active(account.id)

    async def get_account_by_token(self, token: str) -> AccountEntity:
        token_provider = DIAccessTokenProvider.get()
        try:
            account_id = token_provider.decode_token(token)
            account = await self.account_service.get_or_raise_validation(account_id)
            account_session = await self.account_session_service.get_or_create_active(account_id)
            incremented_account_session = account_session.increment_requests()
            await self.account_session_service.save(incremented_account_session, update_fields={"requests"})
            return account
        except AccessControlException as e:
            Logger.auth(
                "auth.token.invalid",
                level=LogMessageLevel.WARN,
                reason=str(e),
            )
            message = AccessControlMessages.invalid_token()
            match str(e):
                case SystemMessages.ACCESS_TOKEN_EXPIRED:
                    message = AccessControlMessages.token_expired()
                case SystemMessages.INVALID_ACCESS_TOKEN:
                    message = AccessControlMessages.invalid_token()
            raise DomainValidationException(
                message=message,
                field=ErrorFields.AUTH_TOKEN
            )
