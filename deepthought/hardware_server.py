from hardware import load
import socket
import time
import os


def process_data(mmc, data):
    """this should have a way to receive function and the parameters from
    client"""

    data_dict = data.loads(data)
    function_name = data["function"]
    arguments = data["arguments"]

    command = "mmc.function_name(**arguments)"
    exec(command)


def run_server(mmc):
    host, port = "localhost", 2500
    print("LISTENING ")
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(2)

        connection, address = server.accept()
        print("Accepted Connection from: ", address)
        while True:
            in_data = connection.recv(1024)
            out_data = process_data(scope, in_data)
            connection.send(out_data)

            time.sleep(1)
        server.close()
    return


if __name__ == "__main__":
    user_dir = os.getcwd()
    mmc = load("configs/demo.cfg")
    print("Microscope loaded.")
    run_server(mmc)
