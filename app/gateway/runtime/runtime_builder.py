from app.gateway.runtime.runtime_device import RuntimeDevice
from app.gateway.runtime.runtime_variable import RuntimeVariable


class RuntimeBuilder:

    @staticmethod
    def build(device, driver):

        runtime = RuntimeDevice(
           device= device,
           driver= driver,
        )

        for variable in device.variables:

            runtime.variables[
                variable.id
            ] = RuntimeVariable(
                id=variable.id,
                name=variable.name,
            )

        driver.runtime = runtime

        return runtime