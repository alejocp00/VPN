import threading
from classes.common.protocols.my_socket import MySocket
from classes.common.protocols.utils import VPNProtocol


socket = MySocket(VPNProtocol.UDP)
socket.bind(("127.0.0.4", 0))

socket.connect(("localhost", 51697))

print("Enviando")
socket.send("2,2".encode())
print("Enviado, recibiendo")
print(socket.recv(1024))
print("Recibido")
socket.close()
