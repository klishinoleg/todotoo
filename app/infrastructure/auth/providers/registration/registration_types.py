# app/infrastructure/auth/providers/registration/registration_types.py
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class RegistrationInitData:
    email: str
    password: str
    confirm_password: Optional[str] = None
    public_name: Optional[str] = None
    language_code: Optional[str] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    start_param: Optional[str] = None
    password_hash: Optional[str] = None
