import MMCorePy
import os
import socket
import SocketServer
import pickle
import time
from contextlib import closing


mm2_path = "C:\Program Files\Micro-Manager-2.0gamma"


class Microscope():
    def __init__(self, config_path):
        self.config_path = os.path.abspath(config_path)
        self.user_dir = os.getcwd()

    def version(self):
        return(self.mmc.getAPIVersionInfo())

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


if __name__ == "__main__":
    def run_scope_command(scope, command):
        exec("scope."+command)
        print("scope."+command)

    scope = Microscope("configs/Bright_Star.cfg")
    scope.load()
    print("Scope loaded")

    host, port = "localhost", 2500

    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(2)

        conn, addr = server.accept()
        while True:
            data = conn.recv(1024)

            if data == "bye":
                break
            if data == "byebye":
                exit()

            elif "mmc" in data.strip():
                comm = run_scope_command(scope, data)
                conn.send(data)
            else:
                print(data)

            time.sleep(1)

        server.close()
