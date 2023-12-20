import socket

# Crear un socket del tipo TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Definir la dirección y el puerto al que nos conectaremos
    server_address = ("localhost", 8080)  # conectar al VPN
    # Conectar al servidor
    client_socket.connect(server_address)

    while True:
        resp1 = client_socket.recv(1024).decode()
        if resp1:
            print(resp1)
            # Recibir un mensaje de la consola
            message = input("> ")
            # Enviar el mensaje al servidor
            client_socket.send(message.encode())

except Exception as e:
    print("Ocurrió un error:", e)

finally:
    # Cerrar la conexión
    client_socket.close()