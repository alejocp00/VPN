import socket

#Crear un socket del tipo TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Definir la dirección y el puerto al que nos conectaremos
server_address = ("localhost", 8080)#conectar al vpn
#Conectar al servidor
client_socket.connect(server_address)


#Recibir un mensaje al servidor
resp1 = client_socket.recv(1024).decode()
print(resp1)
#Recibir un mensaje de la consola
message = input("> ")
#Enviar el mensaje al servidor
client_socket.send(message.encode())
#Recibir un mensaje del servidor
resp2 = client_socket.recv(1024).decode()
print(resp2)
#Recibir un mensaje de la consola
message = input("> ")
#Enviar el mensaje al servidor
client_socket.send(message.encode())
#Recibir un mensaje del servidor
resp3 = client_socket.recv(1024).decode()
print(resp3)
#Recibir un mensaje de la consola
message = input("> ")
#Enviar el mensaje al servidor
client_socket.send(message.encode())

#Cerrar la conexión
client_socket.close()