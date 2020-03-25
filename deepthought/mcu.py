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


def load_mmc(config_path):
    config_abspath = os.path.abspath(config_path)

    # when running in windows computer, the python path has to be mmc path
    # for the drivers to load correctly.

    if os.name == 'nt':
        os.chdir(windows7_path)

    mmc_ = MMCorePy.CMMCore()
    mmc_.loadSystemConfiguration(config_abspath)

    # trick to make the mmc accesible everywhere.
    load_mmc.mmc = mmc_

    return mmc_


def unload_mmc():
    load_mmc.mmc.reset()


def shutdown():
    # unload microscope and exit
    unload_mmc()
    exit()


def parse_command(data_dict):
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

    command_str = 'value = mmc.{}({})'.format(function_name, argument_name)

    return command_str


def execute_command(command_str):
    # function to execute the code in a string
    command = command_str.replace("mmc.", "load_mmc.mmc.")
    value = eval(command)
    return value


def create_mcu_server(mmc):
    server_socket = tcp_server()

    while True:
        client_socket, address = server_socket.accept()
        print("Accepted connection from: ", address)
        server_data = accept_callback(client_socket)

    return


def tcp_server(host="localhost", port=2500):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            serversocket.bind((host, port))

        except OSError:
            port = port + 1
            continue
        break

    serversocket.listen(5)
    print("LISTENING on %s:%s" % (host, port))

    return serversocket


def accept_callback(client):
    # test callback
    while True:
        client_data = client.recv(4096)

        if not client_data:
            break

        elif "shutdown" in str(client_data):
            # safety
            shutdown()

        elif "mmc." in str(client_data):
            # for easy testing thru netcat
            client_data = client_data.decode()
            execute_command(client_data)

        else:
            # the current client comm protocol
            command = parse_command(client_data)
            execute_command(command)


if __name__ == "__main__":
    user_dir = os.getcwd()
    mmc = load_mmc("configs/demo.cfg")
    print("Microscope loaded.")

    try:
        create_mcu_server(mmc)

    except KeyboardInterrupt:
        shutdown()
