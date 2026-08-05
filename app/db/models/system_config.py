from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum as SqlEnum, DateTime
from typing import Optional
from datetime import datetime, timezone

from app.db.models.base import BasePoco, IoTPlatformType


class SystemConfig(BasePoco):
    __tablename__ = "system_configs"

    gateway_name: Mapped[str] = mapped_column(String, comment="Gateway name")
    client_id: Mapped[str] = mapped_column(String, comment="ClientId")
    mqtt_ip: Mapped[str] = mapped_column(String, comment="Mqtt IP")
    mqtt_port: Mapped[int] = mapped_column(Integer, comment="Mqtt port")
    mqtt_uname: Mapped[str] = mapped_column(String, comment="Mqtt username")
    mqtt_upwd: Mapped[str] = mapped_column(String, comment="Mqtt user password")
    iot_platform_type: Mapped[IoTPlatformType] = mapped_column(
        SqlEnum(IoTPlatformType), comment="Platform ouput"
    )

    create_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc))
    create_by: Mapped[Optional[str]] = mapped_column(String(50))
    update_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),)
    update_by: Mapped[Optional[str]] = mapped_column(String(50))