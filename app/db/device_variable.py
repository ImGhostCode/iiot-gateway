from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class DeviceVariable(Base):
    __tablename__ = "device_variables"

    id: Mapped[int] = mapped_column(primary_key=True)

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    address: Mapped[str] = mapped_column(
        String(50)
    )

    data_type: Mapped[str] = mapped_column(
        String(30)
    )

    value: Mapped[str | None]

    device = relationship(
        "Device",
        back_populates="variables",
    )