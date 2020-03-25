import socket


class Controller():
    def __init__(self, mcu_socket):
        self.mcu_socket = mcu_socket

    def setConfig(config_name, config_option):
        cmd = f"mmc.setConfig('setConfig', '{config_name}', '{config_option}')"
        return cmd

    def objective(self, obj):
        cmd = setConfig("objective", obj)
        return self.send_command(cmd)

    def snap(self):
        cmd = "mmc.snapImage()"
        return self.send_command(cmd)

    def image(self):
        cmd = "mmc.getImage()"
        return self.send_command(cmd)

    def moveZ(self, val):
        cmd = f"mmc.setPosition({val})"
        return self.send_command(cmd)

    def moveXY(self, x, y):
        cmd = f"mmc.setXYPosition({x}, {y})"
        return self.send_command(cmd)

    def send_command(self, message):
        self.mcu_socket.sendall(message.encode())
        # wait for a response

        # the response will be, for instance, image in
        # the case of getImage, or None in the case of snapImage
        received = self.mcu_socket.recv(4096).decode()
        return received

    def send(self, message):
        self.mcu_socket.sendall(message)


def connect_to_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def received_data():
    return received


if __name__ == "__main__":
    mcu_socket = connect_to_server("localhost", 2500)
    scope = Controller(mcu_socket)
    scope.send("ping".encode())
