"""
Microscope Control Unit (mcu)

Separates the functions that are essential to communicate to the microscope
using the micromanager API.

This part of the code is in python 2.7 since Micro-manager lacks python3
support for now.

mmc - micro manager core
https://valelab4.ucsf.edu/~MM/doc/MMCore/html/class_c_m_m_core.html

"""
import os
import socket
import MMCorePy


windows7_path = "C:\Program Files\Micro-Manager-2.0gamma"


def load_mmc(config_path):
    # good to operate on the full path of a file - helps in debug
    config_abspath = os.path.abspath(config_path)

    # when running in windows computer, the python path has to be mmc path
    # for the IX83 adapters to load correctly.

    if os.name == 'nt':  # check if windows
        # ah! the microscope computer
        os.chdir(windows7_path)

    # let's load micro-manager stuff
    mmc_ = MMCorePy.CMMCore()
    # the config file which has many abstract microscope functions as
    # config groups
    mmc_.loadSystemConfiguration(config_abspath)

    # trick to make the mmc accesible everywhere, like unload, or
    # execute_comman
    load_mmc.mmc = mmc_

    # not sure if return is needed anymore, given that load_mmc.mmc is
    # pointing at the same object.
    return mmc_


def unload_mmc():
    # in case I need to turn off the server, and safely unload the microscope
    # so that it's ready for the next connection/hwshutdown.
    load_mmc.mmc.reset()


def shutdown():
    # a shutdown sequence
    # unload microscope and exit
    unload_mmc()
    exit()


def parse_command(data_dict):
    # this function needs to be redesigned depending on the new comm protocol.

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

    method_string = 'mmc.{}({})'.format(function_name, argument_name)

    return method_string


def evaluate_mmc(method_string):
    # function evaulates string that is expected to call a method on mmc class

    # mmc is accessible with load_mmc.mmc
    command = method_string.replace("mmc.", "load_mmc.mmc.")

    # catch exceptions here that are related to mmc
    # eval can actually be separated to another function, for easier logging
    # purpose.

    try:
        value = eval(command)

    except:
        return "error:mmc"

    return value


def tcp_server(host="localhost", port=2500):
    # tcp server takes optional host and port

    # a IPv4 TCP socket is created
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # gets rid of the address in use error
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # in case the port is not available, try to bind to the next one
    # do it untill you can bind
    while True:
        try:
            server_socket.bind((host, port))

        except OSError:
            port = port + 1
            continue

        break

    # upto 5 clients can connect (arbitrary for now)
    server_socket.listen(5)

    print("LISTENING on %s %s" % (host, port))
    return server_socket


def accept_callback(client):
    # function that is called after a connection is accepted

    # the main loop
    # the different functions of the server is defined here
    # this can be replaced with a chain of responsibility design pattern

    while True:
        client_data = client.recv(4096)

        if not client_data:
            break

        elif "ping" in str(client_data):
            # testing the connection
            print("pong")

        elif "shutdown" in str(client_data):
            # safety
            shutdown()

        elif "status" in str(client_data):
            # print the status of the microscope
            pass

        elif "mmc." in str(client_data):
            # for directly calling mmc methods
            message = client_data.decode()
            mmc_answer = evaluate_mmc(message)
            send_mmc_answer(mmc_answer)


def create_mcu_server(mmc):
    # manages the client_socket - accepting, closing

    # create a tcp server
    server_socket = tcp_server()

    while True:
        client_socket, address = server_socket.accept()
        print("Accepted connection from: ", address)
        server_data = accept_callback(client_socket)
        client_socket.close()
    return


def send_mmc_answer(mmc_answer):
    # send data to the client

    # not possible to send mmc object over socket because pickling is not
    # an option. (something to do with SWIG/python2.7/mm)

    # but it should be possible to read the attributes of mmc and generate
    # a new object with the data, which can be pickled, and sent to the client.
    # it can be images as numpy arrays, or any other python data structure -
    # like the list of x,y or ZDC offset value, etc.

    # for now, print in console

    print(mmc_answer)
    pass


if __name__ == "__main__":
    user_dir = os.getcwd()

    mmc = load_mmc("configs/demo.cfg")
    print("Microscope loaded.")

    try:
        create_mcu_server(mmc)

    except KeyboardInterrupt:
        shutdown()
