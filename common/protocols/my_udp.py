import socket

class MyUDP:
    def __init__(self, sock=None):
        # Todo: Add the code to initialize the class
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        pass
