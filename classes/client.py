from abc import ABCMeta, abstractmethod
from ctypes import util
from tkinter import Menu
from classes.common.common_variables import *
from classes.common.protocols.my_socket import MySocket
from classes.common.protocols.my_tcp import MyTCP
from classes.common.protocols.my_udp import MyUDP
from classes.common.screen_utils import *


class Client(metaclass=ABCMeta):
    def __init__(self):
        self._config = {
            "client_ip": None,
            "server_ip": VPN_SERVER_IP,
            "server_port": VPN_SERVER_PORT,
            "client_port": None,
            "protocol": VPNProtocol.UNKNOWN,
        }
        self._user_name = ""
        self.__password = ""

    def connect(self):
        """Connect to the server."""
        # Get the user information
        self._user_name = get_user_name() if self._user_name == "" else self._user_name
        self.__password = get_password() if self.__password == "" else self.__password

        # Perform first connection with the vpn
        received_data = self.__perform_first_connection()

        # Parse the received data
        self.__set_configuration(received_data)

        # Connect to the server
        self._connect_to_server()

    def _connect_to_server(self):
        """Connect to the server."""

        self._socket.connect((self._config["server_ip"], self._config["server_port"]))

    def __perform_first_connection(self):
        """Get the VPN protocol."""

        # Instance a new MyTCP socket for the first connection
        self._socket = MySocket(VPNProtocol.TCP)

        # Create the request message
        request_message = self.__create_request_message()

        # Connect the socket to the server
        self._socket.connect((self._config["server_ip"], self._config["server_port"]))

        # Send the request message
        self._socket.send(request_message)

        # Receive the response message
        response_message = self._socket.recv(1024).decode()

        # Process the response
        self.__set_configuration(response_message)

        # Close
        self._socket.close()

    def __create_request_message(self):
        """Create the request message."""
        message = ""

        # Indicate that is a login request
        message += REQUEST_LOGIN_HEADER + REQUEST_SEPARATOR

        # Add the user name
        message += self._user_name + REQUEST_SEPARATOR

        # Add the password
        message += self.__password

        return message.encode()

    def __set_configuration(self, received_data):
        """Set the configuration."""

        if not received_data or received_data == "":
            # Todo: Handle this exception. It can't break the program
            raise Exception("Error: The received data is empty")

        # Split the received data
        received_data = received_data.split(REQUEST_SEPARATOR)

        # Process correct response
        if received_data[0] == REQUEST_ACCEPTED_HEADER:
            # Set the configuration
            self._config["client_ip"] = received_data[1]
            self._config["protocol"] = (
                VPNProtocol.TCP if received_data[2] == "tcp" else VPNProtocol.UDP
            )
            return

        # Process incorrect response
        if received_data[0] == REQUEST_ERROR_HEADER:
            # Todo: Handle this exception. It can't break the program
            raise Exception(f"Error: {received_data[1]}")

    def disconnect(self):
        """Disconnect from the server."""
        self._socket.close()

    @abstractmethod
    def execute_function(self):
        """Execute the client function."""
        pass

    def menu(self):
        """Show the menu."""

        options = [
            "1. Connect to the VPN",
            "2. Execute the client function",
            "3. Disconnect from the VPN",
        ]
        clear_screen()
        print("\n".join(options))
        option = input("Select an option: ")

        while option not in [str(i) for i in range(1, len(options) + 1)]:
            clear_screen()
            self.menu()

        if option == "1":
            self.connect()
        elif option == "2":
            # Todo: Check if the client is connected
            self.execute_function()
        elif option == "3":
            self.disconnect()
        else:
            self.menu()
