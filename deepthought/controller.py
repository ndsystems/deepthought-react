import socket


class TCPControl():
    def __init__(self, host, port):
        self.mcu_socket = self.connect(host, port)

    def connect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def send(self, message):
        self.mcu_socket.sendall(message)

    def recv(self):
        received = self.mcu_socket.recv(4096)
        return received

    def send_command(self, message):
        self.send(message.encode())
        data = self.recv()
        return data

    def serialize(self, data):
        pass

    def deserialize(self, response):
        pass


class Controller(TCPControl):
    def setConfig(config_name, config_option):
        cmd = f"mmc.setConfig('setConfig', '{config_name}', '{config_option}')"
        return cmd

    def objective(self, obj):
        cmd = setConfig("objective", obj)
        return self.send_command(cmd)

    def channel(self, ch):
        cmd = setConfig("channel", ch)
        return self.send_command(cmd)

    def snap(self):
        self.send_command("mmc.snapImage()")
        response = self.send_command("mmc.getImage()")
        image = self.deserialize(response)
        return image

    def moveZ(self, val):
        cmd = f"mmc.setPosition({val})"
        return self.send_command(cmd)

    def moveXY(self, x, y):
        cmd = f"mmc.setXYPosition({x}, {y})"
        return self.send_command(cmd)

    def test(self):
        print(self.send_command("ping").decode())


if __name__ == "__main__":
    scope = Controller("localhost", 2500)
    scope.send("ping".encode())
