from functools import lru_cache

from core.di.email import DIEmailSenderProvider
from interfaces.email.sender import EmailSender


@lru_cache(maxsize=1)
def get_email_sender() -> EmailSender:
    import infrastructure.email  # noqa: F401

    return DIEmailSenderProvider.get()
