import socket


class MyTCP:
    def __init__(self, sock=None):
       
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    def bind(self, addr):
        self.socket.bind(addr)

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

    def connect(self, address):
        self.socket.connect(address)

    def getsockname(self):
        return self.socket.getsockname()
