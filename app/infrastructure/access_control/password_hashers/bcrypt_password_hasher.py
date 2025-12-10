import bcrypt

from core.di.access_control import DIPasswordHasherProvider
from core.enums.di.access_control import PasswordHasherType
from infrastructure.access_control.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())


DIPasswordHasherProvider.register(PasswordHasherType.BCRYPT, BcryptPasswordHasher)
