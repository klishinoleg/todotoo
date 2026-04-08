from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    async def send_email(
            self,
            *,
            to_email: str,
            subject: str,
            text_body: str,
            html_body: str | None = None,
    ) -> None:
        ...
