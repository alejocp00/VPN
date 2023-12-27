from abc import ABCMeta, abstractmethod
from ctypes import util
from tkinter import Menu
from common.common_variables import *
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
        self.__socket = None
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
        # Todo: Implement this method
        pass

    def _connect_to_server(self):
        """Connect to the server."""
        # Todo: Implement this method
        pass

    def __perform_first_connection(self):
        """Get the VPN protocol."""
        # Todo: Implement this method
        pass

    def __set_configuration(self, received_data):
        """Set the configuration."""
        # Todo: Implement this method
        pass

    def disconnect(self):
        """Disconnect from the server."""
        # Todo: Implement this method
        pass

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
