from app.db.models.user import User
from app.repositories.user_repository import UserRepository

from app.schemas.user_dto import UserCreate, UserUpdate
from app.core.security import hash_password

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    async def get_all(self) -> list[User]:
        return await self.repository.get_all()

    async def get_by_id(self, id: str) -> User | None:
        return await self.repository.get_by_id(id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)

    async def create(
        self,
        dto: UserCreate,
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
            role=dto.role,
            gender=dto.gender,
            cell_phone=dto.cell_phone,
            address=dto.address,
            zip_code=dto.zip_code,
            is_active=dto.is_active,
        )

        return await self.repository.create(user)

    async def update(
        self,
        user_id: str,
        dto: UserUpdate,
    ):

        user = await self.repository.get_by_id(
            user_id
        )

        if user is None:
            return None

        data = dto.model_dump(
            exclude_unset=True
        )

        if "password" in data:

            user.password_hash = hash_password(
                data.pop("password")
            )

        for key, value in data.items():
            setattr(user, key, value)

        return await self.repository.update(user)

    async def delete(
        self,
        user_id: str,
    ) -> bool:

        user = await self.repository.get_by_id(
            user_id
        )

        if user is None:
            return False

        await self.repository.delete(user)

        return True