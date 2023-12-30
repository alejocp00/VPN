from abc import ABCMeta, abstractmethod
from ctypes import util
from tkinter import Menu
from common.common_variables import *
from common.protocols.my_tcp import MyTCP
from common.protocols.my_udp import MyUDP
from common.screen_utils import *


class Client(metaclass=ABCMeta):
    def __init__(self):
        self._config = {
            "client_ip": None,
            "server_ip": None,
            "server_port": None,
            "client_port": None,
            "protocol": VPNProtocol.UNKNOWN,
        }
        self._user_name = None
        self.__password = None

    def connect(self):
        """Connect to the server."""
        # Get the user information
        self._user_name = get_user_name() if not self._user_name else self._user_name
        self.__password = get_password() if not self.__password else self.__password

        # Perform first connection with the vpn
        received_data = self.__perform_first_connection()

        # Parse the received data
        self.__set_configuration(received_data)

        # Connect to the server
        self._connect_to_server()

    def _create_socket(self):
        """Create the client socket."""
        if self._config["protocol"] == VPNProtocol.TCP:
            self.__socket = MyTCP()
        elif self._config["protocol"] == VPNProtocol.UDP:
            self.__socket = MyUDP()
        else:
            raise Exception("No socket protocol provided")

    def _connect_to_server(self):
        """Connect to the server."""

        self.__socket.connect((self._config["server_ip"], self._config["server_port"]))

    def __perform_first_connection(self):
        """Get the VPN protocol."""

        # Instance a new MyTCP socket for the first connection
        self.__socket = MyTCP()

        # Create the request message
        request_message = self.__create_request_message()

        # Connect the socket to the server
        self.__socket.connect((self._config["server_ip"], self._config["server_port"]))

        # Send the request message
        self.__socket.sendall(request_message)

        # Receive the response message
        response_message = self.__socket.recv(1024)

        # Process the response
        self.__set_configuration(response_message)

        # Close
        self.__socket.close()

    def __create_request_message(self):
        """Create the request message."""
        # Todo: Implement the request message
        pass

    def __set_configuration(self, received_data):
        """Set the configuration."""
        # Todo: Implement this method
        pass

    def disconnect(self):
        """Disconnect from the server."""
        self.__socket.close()

    @abstractmethod
    def execute_function(self):
        """Execute the client function."""
        pass

    def menu(self):
        """Show the menu."""

        print("1. Connect to a server")
        print("2. Start the service")
        print("3. Disconnect from the server")

        option = input("Option: ")

        while option not in ["1", "2", "3"]:
            clear_screen()
            self.menu()

        if option == "1":
            self.connect()
        elif option == "2":
            self.execute_function()
        elif option == "3":
            self.disconnect()
        else:
            self.menu()
