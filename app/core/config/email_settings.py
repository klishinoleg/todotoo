from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums.di.email import EmailSenderType


class EmailSettings(BaseSettings):
    sender_type: EmailSenderType = EmailSenderType.SMTP
    default_from_email: str = ""
    default_from_name: str = "App"

    smtp_host: str = "localhost"
    smtp_port: int = 25
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = False
    smtp_use_starttls: bool = True
    smtp_timeout_seconds: int = 30
    password_recovery_page_url: str = ""
    password_recovery_ttl_seconds: int = 1800

    model_config = SettingsConfigDict(
        env_prefix="EMAIL_",
        env_file=Path(__file__).parents[2] / ".env",
        extra="ignore",
    )
