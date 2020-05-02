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
import pymmcore
from events import PyMMEventCallBack


windows7_path = "C:\Program Files\Micro-Manager-2.0gamma"
linux_path = "/home/dna/lab/software/micromanager/lib/micro-manager"


class TCPServerCore:
    @staticmethod
    def create_server_socket(host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # gets rid of the address in use error
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)

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
                # repack the SWIG object to make it picklable
                error_msg = "pickling error"
                logging.error(error_msg, exc_info=True)
                serialized_data = error_msg.encode()

        return serialized_data + b"END"


class Microscope:
    def __init__(self, config_path):
        self.working_dir = os.getcwd()

        self.mmc = pymmcore.CMMCore()
        self.config_abspath = os.path.abspath(config_path)

        if os.name == 'nt':  # check if windows
            # ah! the microscope computer
            mm_dir = windows7_path
        elif os.name == "posix":
            mm_dir = linux_path

        os.chdir(mm_dir)
        self.mmc.setDeviceAdapterSearchPaths([mm_dir])
        self.mmc.loadSystemConfiguration(self.config_abspath)
        os.chdir(self.working_dir)

        self.mm_event_callback = PyMMEventCallBack()
        self.mmc.registerCallback(self.mm_event_callback)

    def unload(self):
        # safely unload the microscope
        self.mmc.reset()

    def shutdown(self):
        # a shutdown sequence
        # unload microscope and exit
        self.unload()
        sys.exit()

    def execute(self, command):
        """execute a command, and return the value, or an error"""
        try:
            value = eval(f"self.{command}")
            logging.info(value)

        except Exception as e:
            error_msg = f"MMCore Exception: {command}"
            logging.error(error_msg, exc_info=True)
            return error_msg

        return value


class MicroscopeServer(Microscope, TCPServerCore):
    def __init__(self, config_path, host="localhost", port=2500):
        super().__init__(config_path)
        self.server_socket = self.create_server_socket(host, port)

    def accept_client(self):
        # this loop is for constantly looking for connections
        while True:
            # blocking call
            self.client_socket, self.address = self.server_socket.accept()
            logging.info(f"Accepted connection from: {self.address}")

            while True:
                # this loop is for when we want to keep recv-ing from
                # a connected client
                try:
                    client_data = self.client_socket.recv(300)  # blocking call
                    if not client_data:
                        break

                except (ConnectionResetError):
                    print("Dropped.")
                    break

                response = self.handler(client_data)

                if response == "break":
                    break

    def send(self, data):
        """send data to the client"""
        serialized_data = self.serialize(data)
        self.client_socket.sendall(serialized_data)

    def handler(self, client_data):
        if "ping" in str(client_data):
            # testing the connection
            logging.info("ping")
            self.send("pong\r")

        elif "break" in str(client_data):
            # breaks the recv block
            logging.info("break")
            self.send("breaking client connection\r")
            self.client_socket.shutdown(1)
            return "break"

        elif "shutdown" in str(client_data):
            logging.info("shutdown")
            self.send("shutting down\r")

            self.client_socket.shutdown(1)
            self.shutdown()

        elif "status" in str(client_data):
            logging.info("status")
            response = self.execute("mmc.getSystemState()")
            # temporary workaround

            # a function can take the response, repack it
            # so that a picklable response can be sent
            # thru socket.

            formatted = response.getVerbose()
            formatted = formatted.replace("<br>", "\n")

            self.send(formatted)

        elif "mmc." in str(client_data):
            # for directly calling mmc methods
            request = client_data.decode()
            logging.info(request)
            response = self.execute(request)
            self.send(response)

        else:
            pass


class MultiClientHandler(MicroscopeServer):
    """In case multiple clients have to connect, each with different
     nature of requests (and priority) to the microscope server object

    *   microscope state monitor that checks on the microscope state in a
        regular manner (low priority)

    *   acqusitioncontrol that gives commands passed on by the user
        (high priority)

    *   auto-mechanisms that maintain microscope states - like autofocus,
        auto-exposureTime, autoTrack, etc (medium priority)

    psuedocode:
        while server is on:
            client_socket, request = accept_client()
            queue.append([client_socket, request])

        concurrently, in the queue

        for client_socket, request in queue:
            response = process_request(request)
            send(client_socket, response)
    """
    def __init__():
        self.queue = []


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    scope = MicroscopeServer("configs/demo.cfg")

    try:
        scope.accept_client()

    except KeyboardInterrupt:
        scope.shutdown()
