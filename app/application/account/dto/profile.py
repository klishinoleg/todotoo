from pydantic import BaseModel, Field


class ProfileUpdateRequestDTO(BaseModel):
    public_name: str | None = Field(default=None, max_length=150)
    language: str | None = Field(default=None, max_length=16)
