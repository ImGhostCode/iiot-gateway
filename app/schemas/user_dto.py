from typing import Optional
import uuid

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr

from app.db.models.user import UserRole
from app.db.models.base import GenderEnum


class UserBase(BaseModel):

    name: str

    email: EmailStr

    gender: Optional[GenderEnum] = None

    cell_phone: Optional[str] = None

    address: Optional[str] = None

    zip_code: Optional[str] = None

    role: UserRole = UserRole.VIEWER

    is_active: bool = True


class UserCreate(UserBase):

    password: str


class UserUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[EmailStr] = None

    password: Optional[str] = None

    gender: Optional[GenderEnum] = None

    cell_phone: Optional[str] = None

    address: Optional[str] = None

    zip_code: Optional[str] = None

    role: Optional[UserRole] = None

    is_active: Optional[bool] = None


class UserResponse(UserBase):

    id: uuid.UUID

    model_config = ConfigDict(
        from_attributes=True
    )