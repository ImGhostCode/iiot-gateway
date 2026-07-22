from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum as SqlEnum

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