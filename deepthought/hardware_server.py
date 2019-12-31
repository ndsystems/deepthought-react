from hardware import load
import socket
import time
import os
import pickle


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

    send = pickle.dumps({"value" : value})
    return send


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
            client_data = connection.recv(4096)
            server_data = process_data(mmc, client_data)
            connection.send(server_data)

            time.sleep(1)
    server.close()
    return


if __name__ == "__main__":
    user_dir = os.getcwd()
    mmc = load("configs/demo.cfg")
    print("Microscope loaded.")
    run_server(mmc)
