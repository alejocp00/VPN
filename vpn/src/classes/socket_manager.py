from common.protocols import my_socket


class SocketManager:
    def __init__(self):
        self.__sockets = {}

    def add_socket(self, socket: my_socket.MySocket, name: str):
        self.__sockets[socket] = name

    def clear(self):
        for socket in self.__sockets:
            socket.close()
        self.__sockets = {}
