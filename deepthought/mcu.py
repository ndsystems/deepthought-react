"""
Microscope Control Unit (mcu)

Separates the functions that are essential to operate the microscope for
lower order tasks. This microservice architecture makes it easier to
develop the rest of the codebase, without crashing the microscope hardware
because of exceptions runtime.

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
    """Has the methods that are essential for the communication over TCP"""
    @staticmethod
    def create_server_socket(host, port):
        """Method to create a server side socket"""

        # create a IPv4 TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # gets rid of the address in use error
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)

        # in case the port is not available, try to bind to the next one
        # do it untill an available port is found
        while True:
            try:
                # bind to the host address and port
                server_socket.bind((host, port))

            except Exception as e:
                logging.exception("Exception occurred", exc_info=True)
                port = port + 1
                continue
            break

        # start listening on the bound host address and port
        server_socket.listen(5)
        logging.info(f"LISTENING on {host}:{port}")

        return server_socket

    @staticmethod
    def serialize(data):
        """Appropriate serializing techniques for the data to be sent over
        sockets"""

        # if it is a string, encode it
        if type(data) is str:
            serialized_data = data.encode()

        elif data is None:
            data = "None"
            serialized_data = data.encode()

        # in case of objects
        else:
            # try to pickle them
            try:
                serialized_data = pickle.dumps(data)

            # when it fails, return error
            # failure happens for SWIG objects
            except Exception as e:
                error_msg = "pickling error"
                logging.error(error_msg, exc_info=True)
                serialized_data = error_msg.encode()

        return serialized_data

    def send(self, client_socket, data):
        """send data to the client"""

        # concatinate trailing text so the client side knows where data ends
        serialized_data = self.serialize(data) + b"END"
        client_socket.sendall(serialized_data)


class Microscope:
    """Contains objects necessary for the loading, unloading and communication
    with the microscope (thru pymmcore)"""

    def __init__(self, config_path):
        # use the absolute path of the config_path
        self.config_abspath = os.path.abspath(config_path)

        # store the current working dir, so that we can change it back after
        # device adapters are pointed to the micromanager directory
        # changing the working directory to mm_dir is necessary for pymmcore
        # to find the device adapters (stored in mm_dir) correctly
        self.working_dir = os.getcwd()

        if os.name == 'nt':  # check if windows
            # ah! the microscope computer
            mm_dir = windows7_path
        elif os.name == "posix":
            # the dev's linux computer
            mm_dir = linux_path
        os.chdir(mm_dir)

        # instantiate the micromanager core object, and load the micromanager
        # config file. API is available in
        # https://valelab4.ucsf.edu/~MM/doc/MMCore/html/class_c_m_m_core.html

        self.mmc = pymmcore.CMMCore()
        self.mmc.setDeviceAdapterSearchPaths([mm_dir])
        self.mmc.loadSystemConfiguration(self.config_abspath)

        # change back to the working directory
        os.chdir(self.working_dir)

        # register callback, to catch changes to properties, which can
        # be sourced thru the DataEngine.
        self.mm_event_callback = PyMMEventCallBack()
        self.mmc.registerCallback(self.mm_event_callback)

    def unload(self):
        """safely unload the microscope"""
        self.mmc.reset()

    def execute(self, method):
        """execute a method of MMCore, as instantiated in self.mmc and return
        a result"""
        try:
            # eval executes the method there can be potential security issues
            # here that needs to be looked into
            result = eval(f"self.{method}")
            logging.info(f"{method} : {result}")

        except Exception as e:
            # in case of exception, catch the error, and send a string object
            # with the error message
            error_msg = f"ERROR: {method} : {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

        return result


class MicroscopeServer(Microscope, TCPServerCore):
    """Extends the functionality of Microscope object by making it accessible
    over a server socket"""

    def __init__(self, config_path, host="localhost", port=2500):
        super().__init__(config_path)
        self.server_socket = self.create_server_socket(host, port)

    def shutdown(self):
        """shutdown sequence for MCU"""

        # close the socket, unload the microscope and exit the program
        self.unload()
        sys.exit()

    def accept_client(self):
        """accepts a client, and calls the client handler"""

        # main loop for accepting connections
        # this blocks, disabling multi-client connections

        while True:
            # blocking call
            client_socket, address = self.server_socket.accept()
            logging.info(f"Accepted connection from: {address}")
            self.client_handler(client_socket)

    def client_handler(self, client_socket):
        """receives requests from a client socket, and sends
        response"""

        # client loop for receiving and sending data
        # this is blocking
        while True:
            try:
                client_data = client_socket.recv(300)  # blocking call
                if not client_data:
                    break

            except (ConnectionResetError):
                print("Dropped.")
                break

            # get response from message handler for received data
            # and send it
            response = self.message_handler(client_data)
            self.send(client_socket, response)

    def message_handler(self, client_data):
        """Handles the client messages"""
        request = client_data.decode()
        logging.info(f"REQUEST: {request}")

        if "ping" in str(request):
            # ping the connection - for testing
            return "pong\r"

        elif "shutdown" in str(request):
            # client wants to shutdown server
            self.shutdown()

        elif "mmc." in str(request):
            # message is intended for pymmcore, execute it
            # and return response
            response = self.execute(request)
            return response


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
