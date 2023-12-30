
from common.protocols.my_socket import MySocket
import socket


class MyUDP(MySocket):

    def __init__(self, sock=None):
        # Todo: Add the code to initialize the class
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    def bind(self, ip, port):
        self.socket.bind((ip, port))
    
    def sendto(self, data, ip, port):
        self.socket.sendto(data, (ip, port))

    def recvfrom(self, buffer_size):
        return self.socket.recvfrom(buffer_size)
    
    def close(self):
        self.socket.close()