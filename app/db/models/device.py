from sqlalchemy import (
    Boolean, 
    String,
    Integer
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.base import BaseEntity

class Device(Base, BaseEntity):

    __tablename__ = "devices"

    name: Mapped[str] = mapped_column(String(100))
    
    protocol: Mapped[str] = mapped_column(String(50))

    ip: Mapped[str] = mapped_column(String(50))

    port: Mapped[int] = mapped_column(Integer)

    enable: Mapped[bool] = mapped_column(Boolean)

    polling_interval: Mapped[int] = mapped_column(Integer, default=1000)

    variables = relationship(
        "DeviceVariable",
        back_populates="device",
        cascade="all, delete-orphan"
    )