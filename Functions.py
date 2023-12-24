import socket
import threading
import time
import os

# Variables globales

Log=[] #Historial de lo que ha pasado en el servidor
Socket_list=[] #Lista de sockets abiertos
Thread_list = [] #Lista de hilos abiertos
flag_stop=False #Bandera para indicar que el servidor se va a cerrar
stop_printing = False #Bandera para indicar que se va a dejar de imprimir el historial
stop_printing_lock = threading.Lock() #Lock para la bandera stop_printing
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket del servidor

# Metodo Auxiliar para logear y conectar a los clientes(por ahora no se utilizan los nombres de usuarios y contrasena)

def handle_client(client_socket,protocol):

    #while not flag_stop:   #esto mas adelante va a ser para cuando el servidor cierre indicarle a todos los clientes cerrar el proceso

    try:
        client_socket.send("Introduzca el usuario".encode())
        user = client_socket.recv(1024).decode()
        client_socket.send("Introduzca la contraseña".encode())
        password = client_socket.recv(1024).decode()
        #aqui poner de que comprobar en la bd si no existe ese usuario mandarle error
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
        
    except Exception as e:
        # Cerrar la conexión del cliente cuando se recibe algún error
        Log.append(f"Ocurrió un error:{e}")
        Log.append(f"Cerrando la conexión con el cliente:{client_socket.getpeername()}")
        
    finally:
    # Cerrar la conexión
       client_socket.close()
       Socket_list.remove(client_socket)
       Thread_list.remove(threading.current_thread())

# Metodo Auxiliar para manejar las solicitudes de los clientes

def server_process(server_socket,protocol):
    try:
            while not flag_stop:
                # Aceptar la conexión entrante
                client_socket, client_address = server_socket.accept()
                # Agregando a la lista de logs
                Log.append(f"Nueva conexión aceptada:{client_address}")
                # Agregando a la lista de sockets
                Socket_list.append(client_socket)
                # Iniciar un nuevo hilo para manejar la conexión del cliente
                client_thread = threading.Thread(target=handle_client, args=(Socket_list[-1],protocol,))
                client_thread.start()
                Thread_list.append(client_thread)


    except KeyboardInterrupt:
        # Cerrar el socket del servidor cuando se recibe la señal de interrupción (Ctrl+C)
        Functions.stop()

# Metodo para imprimir los logs

def print_log():
    global stop_printing

    while True:
        os.system('clear')
        with stop_printing_lock:
            if stop_printing:
                stop_printing=False
                break

        for log in Log:
            print(log)
        time.sleep(2)


# Funciones principales del VPN

class Functions:

    def start_server(self):
        # Crear un socket del tipo TCP
        global server_socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Definir la dirección y el puerto en el que el servidor escuchará
        server_address = ("localhost", 8080)
        # Enlazar el socket al servidor
        server_socket.bind(server_address)
        #Elegir el protocolo
        print("Cual protocolo desea utilizar: TCP (use_tcp) , UDP (use_udp)")
        protocol = input("> ")

        # Si quiere regresar al menu
        if(protocol == 'b'):
            server_socket.close()
            return

        # Escuchar conexiones entrantes
        server_socket.listen()

        print("Servidor esperando conexiones en el puerto 8081...")

        server_thread=threading.Thread(target=server_process, args=(server_socket,protocol,))
        server_thread.start()
        Thread_list.append(server_thread)

    # Bases de Metodos todavia no implementados 

    # def create_user(user_name, password):

    #     try:
    #         # Crea un nuevo usuario en la base de datos
    #         user = User(user_name=user_name, password=password)
    #         user.save()
    #         return True
    #     except Exception as e:
    #         print("Ha ocurrido un error creando el usuario:", e)
    #         return False
    
    # def login_user(user_name, password):

    #     try:
    #         # Busca el usuario en la base de datos
    #         user = User.objects.get(user_name=user_name)
    #         #Checkea que la contraseña sea correcta
    #         if user.password == password:
    #            return True
    #         else:
    #            return False
    #     except Exception as e:
    #         print("Ha ocurrido un error logueando el usuario:", e)
    #          return False

    # def restrict_vlan(ID_vlan,IP_network):


    #     # Busca el vlan en la base de datos
    #     vlan = Vlan.objects.get(ID_vlan=ID_vlan)
        
    #     if vlan:
            
    #     else:
            
    # def restrict_user(ID_user,IP_network):


    #     # Busca el usuario en la base de datos
    #     user = User.objects.get(ID_user=ID_user)
        
    #     if user:
            
    #     else:
        
    def log(self):
        global stop_printing # Variable global para detener el hilo de impresión

        # Crear e iniciar el hilo de impresión
        print_thread = threading.Thread(target=print_log)
        print_thread.start()

        while True:
            option = input("> ")
            if option == "b":
                with stop_printing_lock:
                    stop_printing = True # Establecer la flag de control para detener el hilo
                
                print_thread.join()  # Esperar a que el hilo termine antes de retornar
                return

    def stop(self):

        # variables globales que se van a modificar
        global flag_stop
        global server_socket

        # Cerrar todos los sockets
        for socket in Socket_list:
            socket.close()
        Socket_list.clear()

        # Indicar que se detengan todos los procesos de los hilos de los clientes y servidor
        flag_stop=True
        server_socket.close()

        # Esperar a que todos los hilos terminen
        # Esta parte la tengo comentada porque el join da problemas
        print("va a empezar a esperar")
        # for thread in Thread_list:
        #     thread.join()
        Thread_list.clear()
        print("ya termino de esperar")

        # Reestablecer la flag de control
        flag_stop=False
        
        
        

   
    



