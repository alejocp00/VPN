import socket
import threading

def handle_client(client_socket):
    # Recibir datos del cliente
    data = client_socket.recv(1024)
    print(f"Mensaje recibido del cliente: {data.decode()}")
    # Cerrar la conexión del cliente
    client_socket.close()

def start_server():
    # Crear un socket del tipo TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Definir la dirección y el puerto en el que el servidor escuchará
    server_address = ("localhost", 8081)
    # Enlazar el socket al servidor
    server_socket.bind(server_address)
    # Escuchar conexiones entrantes
    server_socket.listen()

    print("Servidor esperando conexiones en el puerto 8081...")

    try:
        while True:
            # Aceptar la conexión entrante
            client_socket, client_address = server_socket.accept()
            print(f"Nueva conexión aceptada: {client_address}")

            # Iniciar un nuevo hilo para manejar la conexión del cliente
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        # Cerrar el socket del servidor cuando se recibe la señal de interrupción (Ctrl+C)
        server_socket.close()

if __name__ == "__main__":
    start_server()