from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.repositories.user_repository import (
    UserRepository,
)

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    SignUpRequest,
    SignUpResponse
)
from app.schemas.user_dto import UserResponse

from app.services.auth_service import (
    AuthService,
)

from app.core.dependencies import (
    get_current_user,
)

router = APIRouter(
    tags=["Authentication"],
)


def get_service(
    db: AsyncSession = Depends(get_db),
):

    return AuthService(
        UserRepository(db)
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(
        get_service
    ),
):
    tokens = await service.login(
        form_data.username,
        form_data.password,
    )

    if tokens is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    return tokens

@router.post(
    "/sign-up",
    response_model=SignUpResponse,
)
async def sign_up(
    request: SignUpRequest,
    service: AuthService = Depends(
        get_service
    ),
):

    try:
        return await service.sign_up(request)

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )

@router.get("/me", response_model=UserResponse)
async def me(
    user = Depends(
        get_current_user
    ),
):
    return user