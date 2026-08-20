import struct

from app.db.models.base import DataTypeEnum, EndianEnum


class ModbusEncoder:

    @staticmethod
    def encode(
        value,
        data_type: DataTypeEnum,
        endian_type: EndianEnum = EndianEnum.None_,
    ) -> list[int]:

        if data_type == DataTypeEnum.Int16:
            registers = [
                int(value) & 0xFFFF
            ]

        elif data_type == DataTypeEnum.Uint16:
            number = int(value)

            if not 0 <= number <= 0xFFFF:
                raise ValueError(
                    f"Uint16 value out of range: {number}"
                )

            registers = [number]

        elif data_type == DataTypeEnum.Int32:
            number = int(value)

            raw = struct.pack(">i", number)

            registers = [
                int.from_bytes(raw[0:2], "big"),
                int.from_bytes(raw[2:4], "big"),
            ]

        elif data_type == DataTypeEnum.Uint32:
            number = int(value)

            if not 0 <= number <= 0xFFFFFFFF:
                raise ValueError(
                    f"Uint32 value out of range: {number}"
                )

            raw = struct.pack(">I", number)

            registers = [
                int.from_bytes(raw[0:2], "big"),
                int.from_bytes(raw[2:4], "big"),
            ]

        elif data_type == DataTypeEnum.Float:
            raw = struct.pack(">f", float(value))

            registers = [
                int.from_bytes(raw[0:2], "big"),
                int.from_bytes(raw[2:4], "big"),
            ]

        elif data_type == DataTypeEnum.Int64:
            number = int(value)

            raw = struct.pack(">q", number)

            registers = [
                int.from_bytes(raw[i:i + 2], "big")
                for i in range(0, 8, 2)
            ]

        elif data_type == DataTypeEnum.Uint64:
            number = int(value)

            if not 0 <= number <= 0xFFFFFFFFFFFFFFFF:
                raise ValueError(
                    f"Uint64 value out of range: {number}"
                )

            raw = struct.pack(">Q", number)

            registers = [
                int.from_bytes(raw[i:i + 2], "big")
                for i in range(0, 8, 2)
            ]

        elif data_type == DataTypeEnum.Double:
            raw = struct.pack(">d", float(value))

            registers = [
                int.from_bytes(raw[i:i + 2], "big")
                for i in range(0, 8, 2)
            ]

        else:
            raise ValueError(
                f"Unsupported Modbus write data type: {data_type}"
            )

        return ModbusEncoder._apply_endian(
            registers,
            endian_type,
        )

    @staticmethod
    def _apply_endian(
        registers: list[int],
        endian_type: EndianEnum,
    ) -> list[int]:

        if endian_type in (
            EndianEnum.None_,
            EndianEnum.BigEndian,
        ):
            return registers

        data = b"".join(
            register.to_bytes(2, "big")
            for register in registers
        )

        if endian_type == EndianEnum.LittleEndian:
            data = data[::-1]

        elif endian_type == EndianEnum.BigEndianSwap:
            data = b"".join(
                data[i:i + 2][::-1]
                for i in range(0, len(data), 2)
            )

        elif endian_type == EndianEnum.LittleEndianSwap:
            words = [
                data[i:i + 2]
                for i in range(0, len(data), 2)
            ]

            words.reverse()

            data = b"".join(words)

        else:
            raise ValueError(
                f"Unsupported endian type: {endian_type}"
            )

        return [
            int.from_bytes(
                data[i:i + 2],
                "big",
            )
            for i in range(0, len(data), 2)
        ]