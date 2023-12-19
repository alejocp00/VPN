import socket

#Crear un socket del tipo TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Definir la dirección y el puerto en el que el servidor escuchará
server_address = ("localhost", 8081)
#Enlazar el socket al servidor
server_socket.bind(server_address)
#Escuchar conexiones entrantes (máximo 1)
server_socket.listen(1)
print("Servidor esperando conexiones en el puerto 8080...")
#Aceptar la conexión entrante
client_socket, client_address = server_socket.accept()
print(client_address)
#Recibir datos del cliente
data = client_socket.recv(1024)
print(f"Mensaje recibido del cliente: {data.decode()}")
#Cerrar conexiones
client_socket.close()
server_socket.close()