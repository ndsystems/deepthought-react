from hardware import Microscope
from view import dd
import socket
import pickle
from contextlib import closing



def from_server(HOST, PORT):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)
    return pickle.loads(data)


# write a live program here.

if __name__ == "__main__":
    scope = from_server("127.0.0.1", 2500)
