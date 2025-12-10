from enum import StrEnum


class AccessTokenType(StrEnum):
    JWT = "jwt"


class PasswordHasherType(StrEnum):
    BCRYPT = "bcrypt"
