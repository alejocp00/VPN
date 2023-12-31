from audioop import add
from common.protocols.my_socket import MySocket
import socket


class MyTCP:
    def __init__(self, sock=None):
        # Todo: Add the code to initialize the class
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    def bind(self, ip, port):
        self.socket.bind((ip, port))

    def listen(self):
        self.socket.listen()

    def accept(self):
        return self.socket.accept()

    def send(self, data):
        self.socket.send(data)

    def recv(self, buffer_size):
        return self.socket.recv(buffer_size)

    def close(self):
        self.socket.close()

    def connect(self, address: tuple[int, int]):
        self.socket.connect(address)
