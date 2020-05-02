"""A microservice to intermediate connections to MCU"""
import socket
import pickle
import time


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
    scope = AcquisitionControl("localhost", 2500)
    scope.setExposure(100)
    scope.image()
    # scope.timelapse(cycles=10, timestep=1)
    img = scope.image()
