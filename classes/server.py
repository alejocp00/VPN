from abc import ABCMeta, abstractmethod
import socket
from classes.common.common_variables import *
from classes.common.protocols.my_socket import MySocket
from classes.common.protocols.my_tcp import MyTCP
from classes.common.protocols.my_udp import MyUDP
from classes.common.screen_utils import *
from classes.socket_manager import SocketManager
from classes.threads_manager import ThreadManager
import threading


class Server(metaclass=ABCMeta):
    def __init__(self, server_ip):
        self.__server_ip = server_ip
        self.__tcp_port = None
        self.__udp_port = None
        self.__thread_manager = ThreadManager()
        self.__socket_manager = SocketManager()
        self.__server_status = VPNStatus.IDLE

    def _start_server(self):
        """Activate the server."""

        self.__server_status = VPNStatus.RUNNING

        # Create the socket
        self._create_sockets()

        # Bind the socket to the port
        self.__socket_tcp.bind((self.__server_ip, 0))
        self.__socket_udp.bind((self.__server_ip, 0))

        # Get the port
        self.__tcp_port = self.__socket_tcp.getsockname()[1]
        self.__udp_port = self.__socket_udp.getsockname()[1]

        self.__socket_tcp.listen()

        # Create a server thread
        server_tcp_thread = threading.Thread(target=self._wait_for_connection)
        server_udp_thread = threading.Thread(target=self._udp_receive_data)

        server_tcp_thread.start()
        server_udp_thread.start()

        self.__thread_manager.add_thread(server_tcp_thread, "server_tcp")
        self.__thread_manager.add_thread(server_udp_thread, "server_udp")

        self.menu()

    def _wait_for_connection(self):
        """Wait for a connection from a client."""
        while self.__server_status == VPNStatus.RUNNING:
            client_socket, client_address = self.__socket_tcp.accept()

            # Add the socket to the socket manager
            self.__socket_manager.add_socket(client_socket, client_address)

            # Create a thread to handle the client
            client_thread = threading.Thread(
                target=self._receive_data, args=(client_socket, client_address)
            )
            client_thread.start()
            self.__thread_manager.add_thread(
                client_thread, "client_" + str(client_address[1])
            )

    def _receive_data(self, client_socket, client_address):
        """Receive data from the client."""

        # Receive the data in small chunks and retransmit it
        data = client_socket.recv(1024).decode()

        # Execute the server function
        result = self._server_function(data, client_socket, client_address)
        msg = self._result_msg(result)
        # Send the data to the client
        client_socket.send(msg.encode())

        # Close the connection
        client_socket.close()

        # Remove the socket from the socket manager
        self.__socket_manager.remove_socket(client_socket)

        # Remove the thread from the thread manager
        self.__thread_manager.remove_thread(threading.current_thread())

    def _udp_receive_data(self):
        """Receive data from clients."""

        while self.__server_status == VPNStatus.RUNNING:
            recv_data, client_address = self.__socket_udp.recv(1024)
            print(client_address)
            if recv_data:
                # Create a thread to handle the client
                client_thread = threading.Thread(
                    target=self.__udp_client_process, args=[recv_data, client_address]
                )
                client_thread.start()

                # Add the thread to the thread manager
                self.__thread_manager.add_thread(
                    client_thread, "client_" + str(client_address)
                )

    def __udp_client_process(self, data, client_address):
        """Process the data received from the client."""
        # Todo: delete this
        print("AQUI")
        # Receive the data in small chunks and retransmit it
        result = self._server_function(data, self.__socket_udp, client_address)
        msg = self._result_msg(result)
        # Send the data to the client
        self.__socket_udp.send(msg.encode(), client_address)

        # Remove the thread from the thread manager
        self.__thread_manager.remove_thread(threading.current_thread())

    def _result_msg(self, result):
        """Create a result message."""
        return REQUEST_RESPONSE_HEADER + REQUEST_SEPARATOR + result

    def _create_sockets(self):
        """Create the server socket."""
        self.__socket_tcp = MySocket(VPNProtocol.TCP)
        # self.__socket_udp = MySocket(VPNProtocol.UDP)
        self.__socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _stop_server(self):
        """Stop the server."""

        # Set the vpn status
        self.__server_status = VPNStatus.SHUTING_DOWN

        # Close all sockets
        self.__socket_manager.clear()

        # Close Threads
        self.__thread_manager.dying_light(True)

        self.__server_status = VPNStatus.IDLE

        self.__tcp_port = None
        self.__udp_port = None

        self.menu()

    @abstractmethod
    def _server_function(self, data, client_socket, client_address) -> str:
        """Execute the server function."""
        pass

    def menu(self):
        """Show the menu."""
        clear_screen()
        print("Server IP: " + self.__server_ip)
        print("TCP port: " + str(self.__tcp_port))
        print("UDP port: " + str(self.__udp_port))

        options = ["1. Start the service", "2. End the service"]

        print("\n".join(options))

        option = input("Option: ")

        while option not in ["1", "2"]:
            clear_screen()
            self.menu()

        if option == "1":
            if self.__server_status == VPNStatus.RUNNING:
                print("The service is already running")
                input("Press enter to continue...")
                self.menu()
            self._start_server()
        elif option == "2":
            self._stop_server()
        else:
            self.menu()
