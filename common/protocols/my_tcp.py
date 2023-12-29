import socket

class MyTCP:
    def __init__(self, sock=None):
        # Todo: Add the code to initialize the class
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        pass
