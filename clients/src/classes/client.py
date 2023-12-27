from abc import ABCMeta, abstractmethod
from common.common_variables import *
from utils.screen_utils import *


class Client(metaclass=ABCMeta):
    def __init__(self):
        self.ip = None
        self.port = None
        self.__socket = None
        self.protocol = VPNProtocol.UNKNOWN
        self._user_name = None
        self.__password = None

    def connect(self):
        """Connect to the server."""
        # Get the user information
        self._user_name = (
            self.get_user_name() if not self._user_name else self._user_name
        )
        self.__password = (
            self.get_password() if not self.__password else self.__password
        )

        # Connect to the server
        self.protocol = self.get_vpn_protocol()

        # Stop connection if the protocol is unknown
        if self.protocol == VPNProtocol.UNKNOWN:
            # Todo: Informar que no se ha conectado al servidor
            return

        # Connect to the server
        self.connect_to_server()

    def get_user_name(self):
        """Get the user name."""

        clear_screen()

        user_name = input("User name: ")

        # Check if the user name is valid
        if not user_name:
            print("The user name is required.")
            return self.get_user_name()

        # Check if the user name was correctly entered
        if "y" != input(f"Is {user_name} correct? (y/n): "):
            return self.get_user_name()

        return user_name

    def get_password(self):
        """Get the password."""

        clear_screen()

        password = input("Password: ")

        # Check if the password is valid
        if not password:
            print("The password is required.")
            return self.get_password()

        return password

    def create_socket(self):
        """Create the client socket."""
        # Todo: Implement this method
        pass

    def connect_to_server(self):
        """Connect to the server."""
        # Todo: Implement this method
        pass

    def get_vpn_protocol(self):
        """Get the VPN protocol."""
        # Todo: Implement this method
        pass

    @abstractmethod
    def execute_function(self, d_ip, d_port, *args):
        """Execute the client function."""
        pass
