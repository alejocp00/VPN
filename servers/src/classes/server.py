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
        while True:
            # Wait for a connection
            self.__connection, self.__client_address = self.__socket.accept()



            self._recieve_data()

            # Close the connection
            self.__connection.close()


    def _recieve_data(self):

        """ Recieve data from the client."""

        # Receive the data in small chunks and retransmit it
        while True:
            data = self.__connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                self.__connection.sendall(data)
            else:
                print('no data from', self.__client_address)
                break

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
        self.__socket.close()


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
