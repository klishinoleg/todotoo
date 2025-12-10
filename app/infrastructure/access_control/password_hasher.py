from abc import ABC, abstractmethod


class PasswordHasher(ABC):

    @staticmethod
    @abstractmethod
    def hash(password: str) -> str:
        ...

    @staticmethod
    @abstractmethod
    def verify(password: str, hashed: str) -> bool:
        ...
