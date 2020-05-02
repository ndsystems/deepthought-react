from handler import BaseHandler


class DeviceProperties(BaseHandler):
    def __init__(self):
        super().__init__(host="localhost", port=2500)

    def get_current_stage_position(self):
        x, y = self.getXYPosition()
        z = self.getPosition()
        return (x, y, z)

    def get_current_exposure_time(self):
        return self.getExposure()

    def get_loaded_devices(self):
        devices = self.getLoadedDevices()

        data = {}
        for device in devices:
            properties = self.getDevicePropertyNames(device)
            data[device] = {prop_name: None for prop_name in properties}
        return data


if __name__ == "__main__":
    state_engine = DeviceProperties()
    print(state_engine.get_current_stage_position())
    print(state_engine.get_current_exposure_time())
    print(state_engine.get_loaded_devices())

    print(state_engine.send_command("mmc.getSystemStateCache()"))
