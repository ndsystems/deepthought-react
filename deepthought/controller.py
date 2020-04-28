import socket
import pickle
import time


class TCPCore:
    def __init__(self, host, port):
        self.mcu_socket = self.connect(host, port)

    def connect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def send(self, message):
        # higher level access to send message to mcu
        self.mcu_socket.sendall(message)

    def recv(self):
        # higher level acesss to recv data from mcu

        received = self.mcu_socket.recv(4096)
        return received


class TCPControl(TCPCore):
    def send_command(self, message):
        # what happens when a command is sent from the controller
        serialized_message = self.serialize(message)
        self.send(serialized_message)
        response = b""

        while True:
            response += self.recv()
            if b"END" in response:
                break

        response = response[:-3]

        data = self.deserialize(response)
        return data

    # this isolates the logic for the communication protocol.
    def serialize(self, message):
        return message.encode()

    def deserialize(self, response):
        try:
            deserialized = response.decode()

        except UnicodeDecodeError:
            deserialized = pickle.loads(response)

        return deserialized


class BaseController(TCPControl):
    @staticmethod
    def setConfig(config_name, config_option):
        cmd = f"mmc.setConfig('setConfig', '{config_name}', '{config_option}')"
        return cmd

    def snapImage(self):
        cmd = "mmc.snapImage()"
        return self.send_command(cmd)

    def getImage(self):
        cmd = "mmc.getImage()"
        return self.send_command(cmd)

    def getPosition(self):
        cmd = f"mmc.getPosition()"
        return self.send_command(cmd)

    def getXYPosition(self):
        cmd = f"mmc.getXYPosition()"
        return self.send_command(cmd)

    def setPosition(self, z_value):
        cmd = f"mmc.setPosition({z_value})"
        return self.send_command(cmd)

    def setXYPosition(self, x, y):
        cmd = f"mmc.setXYPosition({x}, {y})"
        return self.send_command(cmd)

    def setExposure(self, exposure_time):
        cmd = f"mmc.setExposure({exposure_time})"
        return self.send_command(cmd)

    def objective(self, obj):
        cmd = setConfig("objective", obj)
        return self.send_command(cmd)

    def channel(self, ch):
        cmd = setConfig("channel", ch)
        return self.send_command(cmd)


class AcquisitionControl(BaseController):
    def image(self):
        self.snapImage()
        img = self.getImage()
        return img

    def timelapse(self, cycles, timestep):
        # a simple timelapse function
        images = []
        for i in range(cycles):
            snap = self.image()
            print(snap)
            images.append(snap)
            time.sleep(timestep)


if __name__ == "__main__":
    scope = AcquisitionControl("localhost", 2500)
    scope.setExposure(100)
    # scope.timelapse(cycles=10, timestep=1)
    img = scope.image()
    
