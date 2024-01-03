from common.protocols import my_socket


class SocketManager:
    def __init__(self):
        self.__sockets = {}

    def add_socket(self, socket, name: str):
        self.__sockets[socket] = name

    def clear(self):
        for socket in self.__sockets:
            socket.close()
        self.__sockets = {}

    def remove_socket(self, socket):
        if socket in self.__sockets:
            del self.__sockets[socket]
