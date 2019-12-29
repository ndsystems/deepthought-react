from hardware import Microscope
from view import dd
import socket
import pickle
from contextlib import closing

"""
    def channel(self, channel):
        self.mmc.setConfig("channel", channel)

    def objective(self, objective):
        self.mmc.setConfig("objective", objective)

    def snap(self):
        self.mmc.snapImage()
        return self.mmc.getImage()

    def moveZ(self, value):
        self.mmc.setPosition(value)

    def moveXY(self, x, y):
        self.mmc.setXYPosition(x, y)
"""


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
        received = str(self.s.recv(1024))
        return received

    def close(self):
        self.s.close()


# write a live program here.
if __name__ == "__main__":
    server = Connect("localhost", 2500)
    server.connect()
    server.send("""mmc.setConfig("channel", "BF")""")
    # server.send("mmc.snapImage()")
     # server.send("mmc.getImage()")
