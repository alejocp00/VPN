from abc import ABCMeta, abstractmethod
import socket


class MySocket(metaclass=ABCMeta):
    def __init__(self) -> None:
        # fix: need to be raw
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self._socket =socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        # Todo: Implement
        pass

    def send(self):
        # Todo:implement close socket function
        pass


    def close(self):
        # Todo:implement close socket function
        self._socket.close()

    def bind(self, address):
        self._socket.bind(address)

    def listen(self, backlog):
        self._socket.listen(backlog)

    def accept(self):
        return self._socket.accept()

    def connect(self, address):
        self._socket.connect(address)

    def send(self, data):
        self._socket.send(data)

    def recv(self, buffersize):
        return self._socket.recv(buffersize)

    def sendall(self, data):
        self._socket.sendall(data)
