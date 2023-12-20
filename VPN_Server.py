import socket
import threading

def handle_client(client_socket,protocol):

    try:
        client_socket.send("Introduzca el usuario".encode())
        user = client_socket.recv(1024).decode()
        client_socket.send("Introduzca la contraseña".encode())
        password = client_socket.recv(1024).decode()
        client_socket.send("Introduzca el ip al que se quiere conectar".encode())
        ipNetwork = client_socket.recv(1024).decode()
        ipNetwork='localhost'#sobreescribo con este mientras tanto para en otro momento implementar lo del ipnetwork

        if(protocol == 'use_tcp'):
            fake_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            fake_client_address=('127.0.0.8',48656)
            fake_client_socket.bind(fake_client_address)
            fake_client_socket.connect((ipNetwork,8081))

        else:
            fake_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fake_client_address=('127.0.0.8',48656)
            fake_client_socket.bind(fake_client_address)
            fake_client_socket.connect((ipNetwork,8081))
    
    #esta parte de cerrar el socket del cliente todavia no esta del todo bien ya que cuando se deconecta no cierra el socket pq no es como tal una excepcion
    except Exception as e:
        # Cerrar la conexión del cliente cuando se recibe algún error
        print("Ocurrió un error:", e)
        print("Cerrando la conexión con el cliente:", client_socket.getpeername())
    
    finally:
    # Cerrar la conexión
        client_socket.close()


def start_server():
    # Crear un socket del tipo TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Definir la dirección y el puerto en el que el servidor escuchará
    server_address = ("localhost", 8080)
    # Enlazar el socket al servidor
    server_socket.bind(server_address)
    #Elegir el protocolo
    print("Cual protocolo desea utilizar: TCP (use_tcp) , UDP (use_udp)")
    protocol = input("> ")
    # Escuchar conexiones entrantes
    server_socket.listen()

    print("Servidor esperando conexiones en el puerto 8081...")

    try:
        while True:
            # Aceptar la conexión entrante
            client_socket, client_address = server_socket.accept()
            print(f"Nueva conexión aceptada: {client_address}")

            # Iniciar un nuevo hilo para manejar la conexión del cliente
            client_thread = threading.Thread(target=handle_client, args=(client_socket,protocol,))
            client_thread.start()

    except KeyboardInterrupt:
        # Cerrar el socket del servidor cuando se recibe la señal de interrupción (Ctrl+C)
        server_socket.close()

if __name__ == "__main__":
    start_server()