import bcrypt
from datetime import datetime, timezone, timedelta

from jose import jwt

from app.core.config import settings

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")

def verify_password(
    plain,
    hashed,
) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def create_access_token(
    data: dict,
):

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(
    data: dict,
):

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(
    token: str,
):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[
            settings.ALGORITHM
        ],
    )
