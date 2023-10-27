import socket
import pandas as pd

# Generar una lista de números
numeros = [1, 2, 3, 4, 5]

# Crear un DataFrame con los datos
df = pd.DataFrame(numeros, columns=['Numeros'])

# Exportar los datos a un archivo CSV
df.to_csv('numeros.csv', index=False)


#Crear un socket del tipo TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Definir la dirección y el puerto en el que el servidor escuchará
server_address = ("localhost", 8080)
#Enlazar el socket al servidor
server_socket.bind(server_address)
#Escuchar conexiones entrantes (máximo 1)
server_socket.listen(1)
print("Servidor esperando conexiones en el puerto 8080...")
#Aceptar la conexión entrante
client_socket, client_address = server_socket.accept()

#Recibiendo peticiones del cliente

client_socket.send("Cual protocolo desea utilizar: TCP (1) , UDP (2)".encode())
protocol = client_socket.recv(1024)
if protocol == 1:
    TCP=True

client_socket.send("Introduzca el usuario".encode())
user = client_socket.recv(1024)
client_socket.send("Introduzca la contraseña".encode())
password = client_socket.recv(1024)
client_socket.send("Introduzca el ip al que se quiere conectar".encode())
ipNetwork = client_socket.recv(1024)
ipNetwork='localhost'


print(user)
print(password)

#Creando ip falsa

if(TCP):
    fake_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fake_client_address=('127.0.0.8',48656)
    fake_client_socket.bind(fake_client_address)
    fake_client_socket.connect((ipNetwork,8081))

else:
    fake_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fake_client_address=('127.0.0.8',48656)
    fake_client_socket.bind(fake_client_address)
    fake_client_socket.connect((ipNetwork,8081))


#print(f"Mensaje recibido del cliente: {data.decode()}")
#Cerrar conexiones
client_socket.close()
server_socket.close()