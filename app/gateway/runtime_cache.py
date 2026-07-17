class RuntimeCache:
    def __init__(self):
        self.devices = {}

    def update(self, device_id, variables):
        self.devices[device_id] = variables

    def get_device(self, device_id):
        return self.devices.get(device_id, [])
    
    def get_variable(self, device_id, variable_id):
        variables = self.devices.get(device_id, [])
        for variable in variables:
            if variable.id == variable_id:
                return variable
        return None
    

        