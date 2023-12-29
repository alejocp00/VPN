import socket

class MyUDP:
    def __init__(self, sock=None):
        # Todo: Add the code to initialize the class
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        pass

    def bind(self, ip, port):
        self.socket.bind((ip, port))

    def listen(self) :
        self.socket.listen()

    def accept(self):
        return self.socket.accept()
    
    def send(self, data):
        self.socket.send(data)

    def recv(self, buffer_size):
        return self.socket.recv(buffer_size)
    
    def close(self):
        self.socket.close()

    def connect(self, ip, port):
        self.socket.connect((ip, port))
