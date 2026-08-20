from app.gateway.runtime.runtime_device import (
    RuntimeDevice,
)
from app.gateway.runtime.runtime_variable import (
    RuntimeVariable,
)


class RuntimeBuilder:

    @staticmethod
    def build(
        device,
        driver,
    ) -> RuntimeDevice:

        runtime = RuntimeDevice(
            device=device,
            driver=driver,
        )

        for variable in (
            device.device_variables
        ):

            runtime.variables[
                str(variable.id)
            ] = RuntimeVariable(
                id=str(variable.id),
                name=variable.name,
                data_type=variable.data_type
            )

        driver.runtime = runtime

        return runtime