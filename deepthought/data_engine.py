from handler import BaseHandler
from pprint import pprint


class DeviceProperties(BaseHandler):
    def __init__(self):
        super().__init__(host="localhost", port=2500)

    def get_current_stage_position(self):
        x, y = self.getXYPosition()
        z = self.getPosition()
        return (x, y, z)

    def get_current_exposure_time(self):
        return self.getExposure()

    def get_all_properties(self):
        list_of_devices = self.getLoadedDevices()
        all_device_props = {}

        for device in list_of_devices:
            list_of_properties = self.getDevicePropertyNames(device)

            device_props = {}
            for property_ in list_of_properties:
                value = self.getProperty(device, property_)
                device_props[property_] = value

            all_device_props[device] = device_props
        return all_device_props


if __name__ == "__main__":
    state_engine = DeviceProperties()
    pprint(state_engine.get_all_properties())

    # this doesn't work, but should ideally work
