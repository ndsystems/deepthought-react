import MMCorePy
import os
import socket
import pickle
import time
from contextlib import closing

mm2_path = "C:\Program Files\Micro-Manager-2.0gamma"


class Microscope():
    def __init__(self, config_path):
        self.config_path = os.path.abspath(config_path)
        self.user_dir = os.getcwd()

    def version(self):
        self.mmc.getVersionInfo()
        self.mmc.getAPIVersionInfo()

    def load(self):
        self.mmc = MMCorePy.CMMCore()
        # cwd to mm2 path for dlls to load
        os.chdir(mm2_path)
        self.mmc.loadSystemConfiguration(self.config_path)

    def unload(self):
        self.mmc.reset()

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


def create_server(HOST, PORT, scope):
    pickled_data = pickle.dumps(scope)

    while True:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            print("Listening...")
            s.bind((HOST, PORT))
            s.listen(2)
            conn, addr = s.accept()
            with closing(conn):
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(pickled_data)
        time.sleep(1)


if __name__ == "__main__":
    microscope = Microscope("configs/Bright_Star.cfg")

    HOST = '127.0.0.1'
    PORT = 2500
    create_server(HOST, PORT, microscope)
