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
            self._protocol = MyUDP()
            # self._protocol = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            raise NotImplementedError("Protocol not implemented")

        self.protocol = protocol

        pass

    def close(self):
        self._protocol.close()

    def bind(self, address):
        self._protocol.bind(address)

    def listen(self):
        self._protocol.listen()

    def accept(self):
        return self._protocol.accept()

    def connect(self, address):
        self._protocol.connect(address)

    def send(self, data, address="127.0.0.1"):  ###
        if self.protocol == VPNProtocol.UDP:
            self._protocol.send(data, address)
        else:
            self._protocol.send(data)

    def recv(self, buffer_size):
        if self.protocol == VPNProtocol.UDP:
            return self._protocol.recv(buffer_size)
        return self._protocol.recv(buffer_size)

    def getsockname(self):
        return self._protocol.getsockname()

    def get_socket_log(self):
        if self.protocol == VPNProtocol.UDP:
            return self._protocol.log_manager.get_all_log()
