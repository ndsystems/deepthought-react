import socket
import pickle


def command(fn, *args):
    cmd = {
        "function": fn,
        "arguments": args
    }
    return pickle.dumps(cmd)


class Control:
    def __init__(self, server):
        self.server = server

    def command(self, cmd):
        cmd = command(cmd)
        self.server.send(cmd)

    def send_command(self, command):
        self.server.send(command)

    def get_response(self):
        print(self.server.get())

    def channel(channel):
        cmd = command("setConfig", "channel", channel)
        self.send_command(cmd)

    def objective(objective):
        cmd = command("setConfig", "objective", objective)
        self.send_command(cmd)

    def snap(self):
        cmd = command("snapImage")
        self.send_command(cmd)

    def getImage(self):
        cmd = command("getImage")
        self.send_command(cmd)

    def moveZ(value):
        cmd = command("setPosition", value)
        self.send_command(cmd)

    def moveXY(x, y):
        cmd = command("setXYPosition", x, y)
        self.send_command(cmd)


class Connect:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((self.host, self.port))

    def send(self, message):
        self.s.sendall(message)

    def get(self):
        received = pickle.loads(self.s.recv(4096))
        return received

    def close(self):
        self.s.close()


if __name__ == "__main__":
    server = Connect("localhost", 2500)
    server.connect()
    scope = Control(server)
    scope.snap()
