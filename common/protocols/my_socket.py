from abc import ABCMeta, abstractmethod
import socket


class MySocket(metaclass=ABCMeta):
    def __init__(self) -> None:
        # fix: need to be raw
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Todo: Implement
        pass

    def close(self):
        # Todo:implement close socket function
        self._socket.close()
