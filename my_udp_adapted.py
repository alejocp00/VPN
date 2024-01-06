
from common.protocols.my_socket import MySocket
from udp import UDP


class MyUDP(MySocket):

    def __init__(self, sock=None):
        self.socket = UDP()
        self.socket.create_socket()

    def bind(self, ip, port):
        self.socket.udp_bind((ip, port))
    
    def send(self, data, server):
        self.socket.udp_send(data, server)

    def recv(self, buffer_size):
        return self.socket.udp_recv(buffer_size)
    
    def close(self):
        self.socket.close()