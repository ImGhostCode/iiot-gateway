from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from typing import List, Optional
from datetime import datetime,timezone

from app.db.models.base import BasePoco
from app.db.models.device import Device

class Driver(BasePoco):
    __tablename__ = "drivers"

    driver_name: Mapped[str] = mapped_column(String, comment="Driver name")
    file_name: Mapped[str] = mapped_column(String, comment="File name")
    assemble_name: Mapped[str] = mapped_column(String, comment="Folder name")
    authorizes_num: Mapped[int] = mapped_column(Integer, comment="Remaining number of authorizations")

    create_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc))
    create_by: Mapped[Optional[str]] = mapped_column(String(50))
    update_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),)
    update_by: Mapped[Optional[str]] = mapped_column(String(50))

    # Relationship to devices
    devices: Mapped[List["Device"]] = relationship(back_populates="driver")