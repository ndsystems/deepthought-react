"""
Microscope Control Unit (mcu)

Separates the functions that are essential to communicate to the microscope
using the micromanager API.

This part of the code is in python 2.7 since Micro-manager lacks python3
support for now.

"""
import socket
import time
import os
import pickle
import MMCorePy
import os


windows7_path = "C:\Program Files\Micro-Manager-2.0gamma"


def load_config(config_path):
    config_abspath = os.path.abspath(config_path)

    # when running in windows computer, the python path has to be mmc path
    # for the drivers to load correctly.

    if os.name == 'nt':
        os.chdir(windows7_path)

    mmc = MMCorePy.CMMCore()
    mmc.loadSystemConfiguration(config_abspath)
    return mmc


def process_data(mmc, data):
    """this should have a way to receive function and the parameters from
    client"""

    if data == "exit":
        print("Exiting on request")
        exit()

    data_dict = pickle.loads(data)

    function_name = data_dict["function"]
    arguments = data_dict["arguments"]

    argument_name = ''
    for a in arguments:
        if type(a) is str:
            temp = '"{}", '.format(a)
        else:
            temp = '{}, '.format(a)
        argument_name += temp

    argument_name = argument_name[:-2]

    command = 'value = mmc.{}({})'.format(function_name, argument_name)
    exec(command)

    print(command)
    print(value)

    send = pickle.dumps({"value": value})
    return send


def create_mcu_server(mmc):
    host, port = "localhost", 2500
    print("LISTENING ")

    server_socket = tcp_server(host, port)

    while True:
        client_socket, address = server_socket.accept()
        print("Accepted connection from: ", address)
        server_data = accept_callback(client_socket)

    return


def tcp_server(host, port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(5)
    return serversocket


def accept_callback(client):
    # test callback
    while True:
        client_data = client.recv(4096)

        if not client_data:
            break

        if "exit" in str(client_data):
            exit()

        print(client_data)


if __name__ == "__main__":
    user_dir = os.getcwd()
    mmc = load_config("configs/demo.cfg")
    print("Microscope loaded.")

    try:
        create_mcu_server(mmc)

    except KeyboardInterrupt:
        exit()
