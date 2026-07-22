from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as SqlEnum
from typing import Optional

from app.db.models.base import BasePoco, GenderEnum

class User(BasePoco):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(50))
    gender: Mapped[Optional[GenderEnum]] = mapped_column(SqlEnum(GenderEnum))
    cell_phone: Mapped[str] = mapped_column(String)
    home_phone: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(200))
    zip_code: Mapped[str] = mapped_column(String)