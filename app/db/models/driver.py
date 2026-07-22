from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List

from app.db.models.base import BasePoco
from app.db.models.device import Device

class Driver(BasePoco):
    __tablename__ = "drivers"

    driver_name: Mapped[str] = mapped_column(String, comment="Driver name")
    file_name: Mapped[str] = mapped_column(String, comment="File name")
    assemble_name: Mapped[str] = mapped_column(String, comment="Folder name")
    authorizes_num: Mapped[int] = mapped_column(Integer, comment="Remaining number of authorizations")
    
    # Relationship to devices
    devices: Mapped[List["Device"]] = relationship(back_populates="driver")