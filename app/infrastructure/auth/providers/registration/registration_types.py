# app/infrastructure/auth/providers/registration/registration_types.py
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class RegistrationInitData:
    email: str
    password: str
    confirm_password: str
    public_name: Optional[str]
    language_code: Optional[str]
    ip: Optional[str]
    user_agent: Optional[str]
    start_param: Optional[str]
    password_hash: Optional[str]
