from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as SqlEnum, DateTime
from typing import Optional
from datetime import datetime, timezone

from app.db.models.base import BasePoco, GenderEnum

class User(BasePoco):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(50))
    gender: Mapped[Optional[GenderEnum]] = mapped_column(SqlEnum(GenderEnum))
    cell_phone: Mapped[str] = mapped_column(String)
    # home_phone: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(200))
    zip_code: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(50))

    create_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc))
    create_by: Mapped[Optional[str]] = mapped_column(String(50))
    update_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),)
    update_by: Mapped[Optional[str]] = mapped_column(String(50))