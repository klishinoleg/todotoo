from dataclasses import dataclass


@dataclass(slots=True)
class TgUser:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    is_premium: bool | None
    allows_write_to_pm: bool | None
    photo_url: str | None


@dataclass(slots=True)
class TgChat:
    id: int
    type: str
    title: str | None
    username: str | None
    photo_url: str | None


@dataclass(slots=True)
class TelegramInitData:
    user: TgUser
    query_id: str | None
    receiver: TgUser | None
    chat: TgChat | None
    chat_type: str | None
    chat_instance: str | None
    start_param: str | None
    can_send_after: int | None
    auth_date: str
    hash: str | None
    signature: str | None
    init_data: str
