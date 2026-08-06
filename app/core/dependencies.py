from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Request

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token

from app.db.session import get_db

from app.repositories.user_repository import UserRepository

from app.db.models.user import User
from app.db.models.user import UserRole
from app.gateway.device_manager import DeviceManager
from app.gateway.polling_engine import PollingEngine
from app.gateway.event_bus import EventBus

def get_device_manager(request: Request) -> DeviceManager:
    return request.app.state.device_manager

def get_polling_engine(request: Request) -> PollingEngine:
    return request.app.state.polling_engine

def get_event_bus(request: Request) -> EventBus:
    return request.app.state.bus

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    try:

        payload = decode_token(token)

        user_id = str(payload["sub"])

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    repository = UserRepository(db)

    user = await repository.get_by_id(user_id)

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

def require_admin(
    user: User = Depends(
        get_current_user
    ),
):

    if user.role != UserRole.ADMIN:

        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )

    return user

def require_operator(
    user: User = Depends(
        get_current_user
    ),
):

    if user.role not in (
        UserRole.ADMIN,
        UserRole.OPERATOR,
    ):

        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )

    return user