import json

from app.gateway.runtime.raw_value import RawValue
from app.plugins.device_context import DeviceContext
from app.plugins.base_driver import BaseDriver
from app.plugins.config import ConfigParameter

from app.db.models.base import (
    DataSide,
    DataTypeEnum,
)

from app.protocols.modbus.client import ModbusClient
from app.protocols.modbus.decoder import ModbusDecoder
from app.protocols.modbus.mapper import ModbusArea
from app.protocols.modbus.mapper import ModbusMapper
from app.core.logger import logger
from app.protocols.modbus.encoder import ModbusEncoder

class ModbusDriver(BaseDriver):

    @classmethod
    def config_schema(cls):

        return [

            ConfigParameter(
                name="IP",
                description="Modbus TCP server IP address",
                default="127.0.0.1",
            ),

            ConfigParameter(
                name="Port",
                description="Modbus TCP server port",
                default="502",
            ),

            ConfigParameter(
                name="SlaveId",
                description="Modbus slave ID",
                default="1",
            ),

        ]

    async def initialize(self):

        ctx = DeviceContext(self.device)

        self.client = ModbusClient(

            host=ctx.require("IP"),

            port=int(
                ctx.get("Port", 502)
            ),

            slave=int(
                ctx.get("SlaveId", 1)
            ),

        )

    async def connect(self):

        self.connected = await self.client.connect()

    async def disconnect(self):

        if self.connected:

            await self.client.close()

        self.connected = False

    async def read(self) -> list[RawValue]:

        values = []

        for variable in self.device.device_variables:

            response = await self.client.read(variable)

            logger.info(
                f"{variable.method}: "
                f"address={variable.device_address} "
                f"count={ModbusMapper.register_count(variable.data_type)}"
            )

            logger.info(
                f"RESPONSE:{variable.name} === {response}"
            )

            if response.isError():
                raise RuntimeError(
                    f"Modbus read failed for "
                    f"{variable.name}: {response}"
                )


            raw_values = []

            if variable.method in (
                ModbusArea.COIL,
                ModbusArea.DISCRETE_INPUT,
            ):
                raw_values = response.bits[0]
            else:
                raw_values = response.registers

            decoded = ModbusDecoder.decode(
                registers=raw_values,
                data_type=variable.data_type,
            )

            values.append(
                RawValue(
                    variable.id,
                    decoded,
                )
            )

        return values

    async def write(
        self,
        variable,
        value,
    ):

        if not self.connected:
            raise RuntimeError(
                "Modbus device is not connected"
            )

        logger.info(
            f"MODBUS WRITE: "
            f"method={variable.method}, "
            f"address={variable.device_address}, "
            f"type={variable.data_type}, "
            f"endian={variable.endian_type}, "
            f"value={value}"
        )

        if variable.method == ModbusArea.COIL:

            if variable.data_type != DataTypeEnum.Bool:
                logger.warning(
                    f"Coil variable {variable.name} "
                    f"has data type {variable.data_type}"
                )

            response = await self.client.write(
                variable=variable,
                value=value,
            )

            logger.info(
                f"MODBUS WRITE RESPONSE: {response}"
            )

            return response

        if variable.method == ModbusArea.HOLDING_REGISTER:

            registers = ModbusEncoder.encode(
                value=value,
                data_type=variable.data_type,
                endian_type=variable.endian_type,
            )

            logger.info(
                f"ENCODED REGISTERS: "
                f"{registers}"
            )

            response = await self.client.write(
                variable=variable,
                value=value,
                registers=registers,
            )

            logger.info(
                f"MODBUS WRITE RESPONSE: {response}"
            )

            return response

        if variable.method in (
            ModbusArea.DISCRETE_INPUT,
            ModbusArea.INPUT_REGISTER,
        ):

            raise ValueError(
                f"{variable.method} is read-only"
            )

        raise ValueError(
            f"Unsupported Modbus write method: "
            f"{variable.method}"
        )