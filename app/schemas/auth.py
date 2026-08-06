from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import ConfigDict,model_validator
from typing import Optional
import uuid

from app.db.models.user import UserRole
from app.db.models.base import GenderEnum
from app.schemas.user_dto import UserBase

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def validate_identifier(self):
        if not self.email and not self.username:
            raise ValueError("Email or username must be provided.")
        return self


class LoginResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"

class SignUpRequest(BaseModel):

    name: str

    email: EmailStr

    gender: Optional[GenderEnum] = None

    cell_phone: Optional[str] = None

    address: Optional[str] = None

    zip_code: Optional[str] = None

    # role: UserRole = UserRole.VIEWER

    # is_active: bool = True

    password: str

class SignUpResponse(UserBase):

    id: uuid.UUID

    model_config = ConfigDict(
        from_attributes=True
    )