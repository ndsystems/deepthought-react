from hardware import load
import socket
import time
import os


def process_data(scope, data):
    """this should have a way to receive function and the parameters from
    client"""

    data_dict = data.loads(data)
    function_name = data["function"]
    arguments = data["arguments"]

    command = "mmc.function_name(**arguments)"
    exec(command)


def run_server(scope):
    host, port = "localhost", 2500

    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(2)

        connection, address = server.accept()
        while True:
            in_data = connection.recv(1024)
            out_data = process_data(scope, in_data)
            connection.send(out_data)

            time.sleep(1)

        server.close()


user_dir = os.getcwd()
scope = load("configs/demo.cfg")
print("Microscope loaded.")

run_server(scope)
