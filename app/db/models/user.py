# app/db/models/user.py

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.models.base import BasePoco, GenderEnum, UserRole

class User(BasePoco):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(50))

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.ADMIN,
    )

    gender: Mapped[Optional[GenderEnum]] = mapped_column(
        SqlEnum(GenderEnum),
        nullable=True,
    )

    cell_phone: Mapped[Optional[str]] = mapped_column(
        String(30),
        nullable=True,
    )

    address: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    zip_code: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    create_by: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    update_by: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )