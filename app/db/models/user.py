from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin

class User(Base, TimestampMixin):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    
    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


