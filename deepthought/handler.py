"""A microservice to intermediate connections to MCU"""
from configs import get_default
import socket
import pickle
import time

default = get_default()


class TCPClientCore:
    """object that handles the connection aspect of the client socket"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = self.connect()

    def connect(self):
        """initiate a socket connection to the host"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def send(self, message):
        """send message to the server"""
        self.client_socket.sendall(message)

    def recv(self):
        """receive message from the server"""
        received = self.client_socket.recv(4096)
        return received

    def reconnect(self):
        """close the previous connection and open a new one to the host"""
        self.client_socket.close()
        self.client_socket = self.connect()

    def recv_response(self):
        """receive a response for the request"""
        response = b""
        while True:
            response += self.recv()

            # if message end has reached
            if b"END" in response:
                break

        response = response[:-3]
        return response

    def send_request(self, request):
        """send request to the server"""
        serialized_request = self.serialize(request)
        self.send(serialized_request)

        response = self.recv_response()
        data = self.deserialize(response)
        return data

    def serialize(self, message):
        """serialize a message"""
        return message.encode()

    def deserialize(self, response):
        """deserialize a response"""
        try:
            deserialized = response.decode()

        except UnicodeDecodeError:
            deserialized = pickle.loads(response)

        return deserialized


class BaseHandler(TCPClientCore):
    """provides MMCore like API to clients"""

    def setConfig(self, config_name, config_option):
        cmd = f"mmc.setConfig('setConfig', '{config_name}', '{config_option}')"
        return self.send_request(cmd)

    def getProperty(self, device_label, property_name):
        cmd = f"mmc.getProperty('{device_label}', '{property_name}')"
        return self.send_request(cmd)

    def getDevicePropertyNames(self, device_label):
        cmd = f"mmc.getDevicePropertyNames('{device_label}')"
        return self.send_request(cmd)

    def getLoadedDevices(self):
        cmd = "mmc.getLoadedDevices()"
        return self.send_request(cmd)

    def snapImage(self):
        cmd = "mmc.snapImage()"
        return self.send_request(cmd)

    def getImage(self):
        cmd = "mmc.getImage()"
        return self.send_request(cmd)

    def getPosition(self):
        cmd = f"mmc.getPosition()"
        return self.send_request(cmd)

    def getXYPosition(self):
        cmd = f"mmc.getXYPosition()"
        return self.send_request(cmd)

    def setPosition(self, z_value):
        cmd = f"mmc.setPosition({z_value})"
        return self.send_request(cmd)

    def setXYPosition(self, x, y):
        cmd = f"mmc.setXYPosition({x}, {y})"
        return self.send_request(cmd)

    def getExposure(self):
        cmd = f"mmc.getExposure()"
        return self.send_request(cmd)

    def setExposure(self, exposure_time):
        cmd = f"mmc.setExposure({exposure_time})"
        return self.send_request(cmd)

    def objective(self, obj):
        cmd = self.setConfig("objective", obj)
        return self.send_request(cmd)

    def channel(self, ch):
        cmd = self.setConfig("channel", ch)
        return self.send_request(cmd)

    def startContinuousSequenceAcquisition(self, value):
        cmd = f"mmc.startContinuousSequenceAcquisition({value})"
        return self.send_request(cmd)

    def getRemainingImageCount(self):
        cmd = f"mmc.getRemainingImageCount()"
        return self.send_request(cmd)

    def getLastImage(self):
        cmd = f"mmc.getLastImage()"
        return self.send_request(cmd)

    def stopSequenceAcquisition(self):
        cmd = f"mmc.stopSequenceAcquisition()"
        return self.send_request(cmd)

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


class AcquisitionControl(BaseHandler):
    """example usage of BaseHandler"""

    def image(self):
        self.snapImage()
        img = self.getImage()
        return img

    def timelapse(self, cycles, timestep):
        # a simple timelapse function which is very much blocking
        images = []
        for i in range(cycles):
            snap = self.image()
            print(snap)
            images.append(snap)
            time.sleep(timestep)


if __name__ == "__main__":
    # run debug mcu with:
    # This will open a socket server and listen on the mcu: host and mcuport
    #
    #   $ python run_mcu.py
    #
    # run debug client with python -i handler.py
    #
    # which run the file, then open up the python
    # interpreter, where you can write code on top of handler.py.
    #
    # In this case, this main function creates an instance of AcquisitionControl class that will
    # establish a connection to mcu at the host and port of the MCU server as defined in the config.

    hostname = default["mcu_server"]["hostname"]
    port = int(default["mcu_server"]["port"])

    scope = AcquisitionControl(hostname, port)
