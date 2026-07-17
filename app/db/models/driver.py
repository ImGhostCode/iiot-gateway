from sqlalchemy import(
    String,
    Integer
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.models.base import BaseEntity

class Driver(Base, BaseEntity):

    __tablename__ = "drivers"

    driver_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )
    file_name: Mapped[str] = mapped_column(
        String(200)
    )
    assemble_name: Mapped[str] = mapped_column(
        String(200)
    )
    authorize_num: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    devices = relationship(
        "Device",
        back_populates="driver"
    )
