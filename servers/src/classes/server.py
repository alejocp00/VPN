from abc import ABCMeta, abstractmethod
from common.common_variables import *
from common.protocols.my_tcp import MyTCP
from common.protocols.my_udp import MyUDP
from common.screen_utils import *
from vpn.src.classes.socket_manager import SocketManager
from vpn.src.classes.threads_manager import ThreadManager
import threading


class Server(metaclass=ABCMeta):
    def __init__(self):
        self._config = {
            "server_ip": None,
            "server_port": None,
            "protocol": VPNProtocol.UNKNOWN,
        }
        self.__thread_manager = ThreadManager()
        self.__socket_manager = SocketManager()
        self.__vpn_status = VPNStatus.IDLE

    def _start_server(self):
        """ Activate the server."""

        # Create the socket
        self._create_socket()

        # Bind the socket to the port
        self.__socket.bind((self._config["server_ip"], self._config["server_port"]))
        
        # Listen for incoming connections
        self.__socket.listen()

        # Create a server thread
        server_thread = threading.Thread(target=self._wait_for_connection)
        server_thread.start()
        self.__thread_manager.add_thread(server_thread, "server")

    def _wait_for_connection(self):
        """ Wait for a connection from a client."""

        while self.__vpn_status == VPNStatus.RUNNING:

            client_socket, client_address = self.__socket.accept()

            # Add the socket to the socket manager
            self.__socket_manager.add_socket(client_socket, client_address)

            # Create a thread to handle the client
            client_thread = threading.Thread(
                target=self._recieve_data , args=(client_socket, client_address)
            )
            client_thread.start()
            self.__thread_manager.add_thread(client_thread, "client")

    def _recieve_data(self, client_socket, client_address):

        """ Recieve data from the client."""

        # Receive the data in small chunks and retransmit it
        while self.__vpn_status == VPNStatus.RUNNING:
            data = client_socket.recv(16)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                client_socket.sendall(data)
            else:
                print('no data from', client_address)
                break
        
        # Close the connection
        client_socket.close()

        # Remove the socket from the socket manager
        self.__socket_manager.remove_socket(client_socket)

        # Remove the thread from the thread manager
        self.__thread_manager.remove_thread(threading.current_thread())

    def _create_socket(self):
        """Create the server socket."""
        if self._config["protocol"] == VPNProtocol.TCP:
            self.__socket = MyTCP()
        elif self._config["protocol"] == VPNProtocol.UDP:
            self.__socket = MyUDP()
        else:
            raise Exception("No socket protocol provided")

    def _stop_server (self):
        """ Stop the server."""

        # Set the vpn status
        self.__vpn_status = VPNStatus.SHUTING_DOWN

        # Close all sockets
        self.__socket_manager.clear()

        # Close Threads
        self.__thread_manager.dying_light(True)

        self.__vpn_status = VPNStatus.IDLE

        self.menu


    def menu(self):
        """Show the menu."""

        print("1. Start the service")
        print("2. End the service")

        option = input("Option: ")

        while option not in ["1", "2"]:
            clear_screen()
            self.menu()

        if option == "1":
            self._start_server()
        elif option == "2":
            self._stop_server()
        else:
            self.menu()
