from classes.common.protocols.my_tcp import MyTCP
from classes.common.protocols.my_udp import MyUDP
from classes.common.protocols.utils import VPNProtocol
import socket


class MySocket:
    def __init__(self, protocol: VPNProtocol) -> None:
        # Selecting the protocol to use
        if protocol == VPNProtocol.TCP:
            self._protocol = MyTCP()
        elif protocol == VPNProtocol.UDP:
            # self._protocol = MyUDP()
            # self._protocol.create_socket()
            self._protocol = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            raise NotImplementedError("Protocol not implemented")

        self.protocol = protocol

        # Todo: Implement
        pass

    def close(self):
        # Todo:implement close socket function
        self._protocol.close()

    def bind(self, address):
        self._protocol.bind(address)

    def listen(self):
        self._protocol.listen()

    def accept(self):
        return self._protocol.accept()

    def connect(self, address):
        self._protocol.connect(address)

    def send(self, data):
        if self.protocol == VPNProtocol.UDP:
            self._protocol.send(data)
        else:
            self._protocol.send(data)

    def recv(self, buffer_size):
        return self._protocol.recv(buffer_size)

    def sendall(self, data):
        self._protocol.sendall(data)

    def getsockname(self):
        return self._protocol.getsockname()
