from __future__ import annotations

import asyncio
import smtplib
import ssl
from email.message import EmailMessage

from core.config.settings import settings
from core.di.email import DIEmailSenderProvider
from core.enums.di.email import EmailSenderType
from interfaces.email.sender import EmailSender


class SmtpEmailSender(EmailSender):
    async def send_email(
            self,
            *,
            to_email: str,
            subject: str,
            text_body: str,
            html_body: str | None = None,
    ) -> None:
        await asyncio.to_thread(
            self._send_sync,
            to_email=to_email,
            subject=subject,
            text_body=text_body,
            html_body=html_body,
        )

    @staticmethod
    def _build_message(to_email: str, subject: str, text_body: str, html_body: str | None = None) -> EmailMessage:
        msg = EmailMessage()
        from_name = settings.email.default_from_name.strip()
        from_email = settings.email.default_from_email.strip()
        if from_name:
            msg["From"] = f"{from_name} <{from_email}>"
        else:
            msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(text_body)
        if html_body:
            msg.add_alternative(html_body, subtype="html")
        return msg

    def _send_sync(self, *, to_email: str, subject: str, text_body: str, html_body: str | None = None) -> None:
        msg = self._build_message(to_email=to_email, subject=subject, text_body=text_body, html_body=html_body)
        timeout = settings.email.smtp_timeout_seconds
        host = settings.email.smtp_host
        port = settings.email.smtp_port

        if settings.email.smtp_use_tls:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host=host, port=port, timeout=timeout, context=context) as server:
                self._login_if_needed(server)
                server.send_message(msg)
            return

        with smtplib.SMTP(host=host, port=port, timeout=timeout) as server:
            if settings.email.smtp_use_starttls:
                context = ssl.create_default_context()
                server.starttls(context=context)
            self._login_if_needed(server)
            server.send_message(msg)

    @staticmethod
    def _login_if_needed(server: smtplib.SMTP) -> None:
        username = settings.email.smtp_username.strip()
        password = settings.email.smtp_password
        if username:
            server.login(username, password)


DIEmailSenderProvider.register(EmailSenderType.SMTP, SmtpEmailSender)
