from pydantic import BaseModel

from application.account.dto.account import AccountDTO
from application.account.dto.account_auth_profile import AccountAuthProfileDTO


class AuthResponseDTO(BaseModel):
    """
    Final authentication response DTO.
    Contains the account, the provider profile, and the issued token.
    """
    account: AccountDTO
    auth: AccountAuthProfileDTO
    token: str
