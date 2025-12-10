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
