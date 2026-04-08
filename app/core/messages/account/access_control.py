from core.enums.app.account.auth_provider import AuthProviderType
from core.i18n import _


class AccessControlMessages:
    @classmethod
    def invalid_auth_provider_data(cls, auth_provider_type: AuthProviderType) -> str:
        return str(_("Invalid auth provider data for provider: {}").format(auth_provider_type.get_label()))

    @classmethod
    def account_auth_profile_not_found(cls) -> str:
        return str(_("Account auth profile not found"))

    @staticmethod
    def invalid_token() -> str:
        return str(_("Invalid token"))

    @staticmethod
    def token_expired() -> str:
        return str(_("Token expired"))

    @staticmethod
    def no_credentials_provided() -> str:
        return str(_("No credentials provided"))

    @staticmethod
    def account_not_found(info: str | int = "") -> str:
        return str(_("Account not found {}").format(str(info)).strip())

    @staticmethod
    def telegram_invalid_hash() -> str:
        return str(_("Invalid Telegram hash"))

    @staticmethod
    def telegram_auth_expired() -> str:
        return str(_("Telegram auth expired"))

    @staticmethod
    def password_auth_profile_not_found() -> str:
        return str(_("Password profile not found"))

    @staticmethod
    def invalid_username_or_password() -> str:
        return str(_("Invalid username or password"))

    @staticmethod
    def auth_profile_does_not_belong_to_account() -> str:
        return str(_("Auth profile does not belong to this account"))

    @staticmethod
    def cannot_delete_last_auth_profile() -> str:
        return str(_("You cannot delete the last auth profile"))

    @staticmethod
    def auth_profile_merge_confirmation_required(account_id: int) -> str:
        return str(
            _(
                "This auth profile is linked to another account (id={}). "
                "If you continue, that account and all its activity will be deleted. "
                "Repeat request with confirm_merge=true."
            ).format(account_id)
        )

    @staticmethod
    def auth_provider_already_linked(provider_type: AuthProviderType) -> str:
        return str(_("Auth profile for provider already linked: {}").format(provider_type.get_label()))
