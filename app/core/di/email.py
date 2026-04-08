from core.config.settings import settings
from core.enums.di.email import EmailSenderType
from core.exceptions.system import RepositoryException
from core.messages.system.no_localized_messages import SystemMessages
from interfaces.email.sender import EmailSender


class DIEmailSenderProvider:
    _providers: dict[EmailSenderType, type[EmailSender]] = {}

    @classmethod
    def register(cls, sender_type: EmailSenderType, provider: type[EmailSender]) -> None:
        cls._providers[sender_type] = provider

    @classmethod
    def get(cls, sender_type: EmailSenderType | None = None) -> EmailSender:
        if sender_type is None:
            sender_type = settings.email.sender_type

        provider_cls = cls._providers.get(sender_type)
        if provider_cls is None:
            raise RepositoryException(SystemMessages.EMAIL_SENDER_PROVIDER_NOT_REGISTERED)
        return provider_cls()
