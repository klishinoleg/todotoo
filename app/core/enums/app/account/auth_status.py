from enum import StrEnum


class AuthMailStatus(StrEnum):
    SENT = "sent"
    RESET = "reset"


class AuthPasswordStatus(StrEnum):
    SET = "set"
    CHANGED = "changed"


class AuthProfileLinkStatus(StrEnum):
    LINKED = "linked"
    ALREADY_LINKED = "already_linked"
    CONFIRMATION_REQUIRED = "confirmation_required"


class AuthProfileDeleteStatus(StrEnum):
    DELETED = "deleted"
