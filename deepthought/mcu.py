"""
Microscope Control Unit (mcu)

Separates the functions that are essential to operate the microscope
for specific higher order tasks, mostly wrapping around micromanager API.

mmc - micro manager core
https://valelab4.ucsf.edu/~MM/doc/MMCore/html/class_c_m_m_core.html

problems: pickling swig objects
https://stackoverflow.com/questions/9310053/how-to-make-my-swig-extension-module-work-with-pickle

"""
import os
import sys
import logging
import socket
import pickle
import MMCorePy

windows7_path = "C:\Program Files\Micro-Manager-2.0gamma"


class TCPServerCore:
    @staticmethod
    def create_socket(host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # gets rid of the address in use error
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # in case the port is not available, try to bind to the next one
        # do it untill an available port is found
        while True:
            try:
                server_socket.bind((host, port))

            except Exception as e:
                logging.exception("Exception occurred", exc_info=True)
                port = port + 1
                continue
            break

        # upto 5 clients can connect (arbitrary for now)
        server_socket.listen(5)

        logging.info(f"LISTENING on {host}:{port}")
        return server_socket


class Microscope:
    def __init__(self, config_path):
        self.mmc = MMCorePy.CMMCore()
        self.config_abspath = os.path.abspath(config_path)

        if os.name == 'nt':  # check if windows
            # ah! the microscope computer
            os.chdir(windows7_path)

        self.mmc.loadSystemConfiguration(self.config_abspath)

    def unload(self):
        # safely unload the microscope
        self.mmc.reset()

    def shutdown(self):
        # a shutdown sequence
        # unload microscope and exit
        self.unload()
        sys.exit()

    def execute(self, command):
        try:
            value = eval(f"self.{command}")

        except Exception as e:
            error_msg = f"unknown mmc command: {command}"
            logging.error(error_msg, exc_info=True)
            return error_msg

        return value


class MicroscopeServer(Microscope):
    def __init__(self, config_path, host="localhost", port=2500):
        super().__init__(config_path)
        self.host = host
        self.port = port
        self.client_socket = None
        self.address = None

    def startServer(self):
        server = TCPServerCore()
        server_socket = server.create_socket(self.host, self.port)

        # this loop is for constantly looking for connections
        while True:
            # blocking call
            self.client_socket, self.address = server_socket.accept()
            logging.info(f"Accepted connection from: {self.address}")
            server_data = self.callback()

    @staticmethod
    def serialize(data):
        if type(data) is str:
            serialized_data = data.encode()

        elif data is None:
            data = "None"
            serialized_data = data.encode()

        else:
            try:
                serialized_data = pickle.dumps(data)

            except Exception as e:
                error_msg = "pickling error"
                logging.error(error_msg, exc_info=True)
                serialized_data = error_msg.encode()

        return serialized_data + b"END"

    def send(self, reply):
        """send data to the client"""
        serialized_mmc_reply = self.serialize(reply)
        print(reply)
        self.client_socket.sendall(serialized_mmc_reply)

    def callback(self):
        """function that is called after a connection is accepted"""

        # the main loop
        # the different functions of the server is defined here
        # this can be replaced with a chain of responsibility design pattern

        while True:
            # this loop is for when we want to keep recv-ing from a connected
            # client

            try:
                client_data = self.client_socket.recv(300)  # blocking call

                if not client_data:
                    break

            except (ConnectionResetError):
                print("Dropped.")
                break

            if "ping" in str(client_data):
                # testing the connection
                logging.info("ping")
                self.send("pong\r")

            elif "break" in str(client_data):
                # breaks the recv block
                logging.info("break")
                self.send("breaking\r")
                self.client_socket.shutdown(1)
                break

            elif "shutdown" in str(client_data):
                logging.info("shutdown")
                self.send("shutting down\r")
                self.client_socket.shutdown(1)
                self.shutdown()

            elif "status" in str(client_data):
                logging.info("status")
                mmc_reply = self.execute("mmc.getSystemState()")
                formatted = mmc_reply.getVerbose()
                formatted = formatted.replace("<br>", "\n")
                self.send(formatted)

            elif "mmc." in str(client_data):
                # for directly calling mmc methods
                command = client_data.decode()
                logging.info(command)
                mmc_reply = self.execute(command)
                self.send(mmc_reply)
            else:
                pass


if __name__ == "__main__":
    user_dir = os.getcwd()
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    scope = MicroscopeServer("configs/demo.cfg")

    try:
        scope.startServer()

    except KeyboardInterrupt:
        scope.shutdown()
