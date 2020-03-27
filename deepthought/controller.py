import socket
import pickle


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
    # this isolates the logic for the communication protocol.

    def send_command(self, message):
        # what happens when a command is sent from the controller

        serialized_message = self.serialize(message)
        self.send(serialized_message)

        response = self.recv()
        data = self.deserialize(response)
        return data

    def serialize(self, message):
        return message.encode()

    def deserialize(self, response):
        print(response)  # for debugging


class BaseController(TCPControl):
    @staticmethod
    def setConfig(config_name, config_option):
        cmd = f"mmc.setConfig('setConfig', '{config_name}', '{config_option}')"
        return cmd

    def snapImage(self):
        response = self.send_command("mmc.snapImage()")
        return response

    def getImage(self):
        response = self.send_command("mmc.getImage()")
        image = self.deserialize(response)
        return image

    def setPosition(self, val):
        cmd = f"mmc.setPosition({val})"
        return self.send_command(cmd)

    def setXYPosition(self, x, y):
        cmd = f"mmc.setXYPosition({x}, {y})"
        return self.send_command(cmd)

    def objective(self, obj):
        cmd = setConfig("objective", obj)
        return self.send_command(cmd)

    def channel(self, ch):
        cmd = setConfig("channel", ch)
        return self.send_command(cmd)


class DebugControl(BaseController):
    def test(self):
        print(self.send_command("ping"))


if __name__ == "__main__":
    scope = DebugControl("localhost", 2500)
    scope.test()
