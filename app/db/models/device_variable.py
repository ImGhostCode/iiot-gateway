# app/db/models/device_variable.py

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.base import BaseEntity

class DeviceVariable(Base, BaseEntity):

    __tablename__ = "device_variables"

    name: Mapped[str]

    description: Mapped[str | None]

    method: Mapped[str]

    device_address: Mapped[str]

    data_type: Mapped[str]

    is_trigger: Mapped[bool]

    endian_type: Mapped[str]

    expressions: Mapped[str | None]

    is_upload: Mapped[bool]

    protect_type: Mapped[str]

    index: Mapped[int] = mapped_column(Integer)

    alias: Mapped[str | None]

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    device = relationship(
        "Device",
        back_populates="variables",
    )