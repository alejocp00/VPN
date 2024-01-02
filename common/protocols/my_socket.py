from common.protocols.my_tcp import MyTCP
from common.protocols.my_udp import MyUDP
from common.protocols.utils import VPNProtocol
import socket


class MySocket:
    def __init__(self, protocol: VPNProtocol) -> None:
        # Selecting the protocol to use
        if protocol == VPNProtocol.TCP:
            self._protocol = MyTCP()
        elif protocol == VPNProtocol.UDP:
            self._protocol = MyUDP()
        else:
            raise NotImplementedError("Protocol not implemented")

        # fix: need to be raw
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Todo: Implement
        pass

    def close(self):
        # Todo:implement close socket function
        self._socket.close()

    def bind(self, address):
        self._socket.bind(address)

    def listen(self, backlog):
        self._socket.listen(backlog)

    def accept(self):
        return self._socket.accept()

    def connect(self, address):
        self._socket.connect(address)

    def send(self, data):
        self._socket.send(data)

    def recv(self, buffersize):
        return self._socket.recv(buffersize)

    def sendall(self, data):
        self._socket.sendall(data)
