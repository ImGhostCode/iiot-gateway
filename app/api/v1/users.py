from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.user_repository import (
    UserRepository,
)

from app.schemas.user_dto import (
    UserCreate,
    UserResponse,
    UserUpdate,
)

from app.services.user_service import (
    UserService,
)

from app.core.dependencies import get_current_user, require_admin

router = APIRouter(
    tags=["Users"]
)


def get_service(
    db: AsyncSession = Depends(get_db),
):
    return UserService(
        UserRepository(db)
    )


@router.get(
    "/",
    response_model=list[UserResponse],
)
async def get_users(
    service: UserService = Depends(
        get_service
    ),
    admin=Depends(
        require_admin
    ),
):

    return await service.get_all()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: str,
    admin=Depends(
        require_admin
    ),
    service: UserService = Depends(
        get_service
    ),
):

    user = await service.get_by_id(
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    dto: UserCreate,
    admin=Depends(
        require_admin
    ),
    service: UserService = Depends(
        get_service
    ),
):

    try:
        return await service.create(dto)

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: str,
    dto: UserUpdate,
    admin=Depends(
        require_admin
    ),
    service: UserService = Depends(
        get_service
    ),
):

    user = await service.update(
        user_id,
        dto,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: str,
    admin=Depends(
        require_admin
    ),
    service: UserService = Depends(
        get_service
    ),
):

    deleted = await service.delete(
        user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )