# app/db/models/device_config.py

from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.base import BaseEntity


class DeviceConfig(Base, BaseEntity):

    __tablename__ = "device_configs"

    device_config_name: Mapped[str]

    data_side: Mapped[int]

    description: Mapped[str | None]

    value: Mapped[str | None]

    enum_info: Mapped[str | None]

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    device = relationship(
        "Device",
        back_populates="configs",
    )