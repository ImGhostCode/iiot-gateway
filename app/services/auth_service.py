from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)

from app.repositories.user_repository import (
    UserRepository,
)
from app.schemas.auth import SignUpRequest
from app.db.models.user import User
from app.db.models.base import UserRole
from app.core.security import hash_password

class AuthService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def login(
        self,
        email: str,
        password: str,
    ):

        user = await self.repository.get_by_email(
            email
        )

        if user is None:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        payload = {
            "sub": str(user.id),
            "role": user.role.value,
        }

        return {
            "access_token":
                create_access_token(payload),

            "refresh_token":
                create_refresh_token(payload),
        }

    async def sign_up(
        self,
        dto:  SignUpRequest, 
    ):
        existed = await self.repository.get_by_email(
            dto.email
        )

        if existed:
            raise ValueError(
                "Email already exists."
            )

        user = User(
            name=dto.name,
            email=dto.email,
            password_hash=hash_password(
                dto.password
            ),
            role= UserRole.VIEWER,
            gender=dto.gender,
            cell_phone=dto.cell_phone,
            address=dto.address,
            zip_code=dto.zip_code,
            is_active= True,
        )

        return await self.repository.create(user)
