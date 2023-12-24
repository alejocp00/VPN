from common.common_variables import *
from utils.screen_utils import *


class Client:
    def __init__(self, function):
        self.client_function = function
        self.ip = None
        self.port = None
        self.socket = None
        self.protocol = (
            vpn_protocol if vpn_protocol != VPNProtocol.UNKNOWN else VPNProtocol.TCP
        )

    def connect(self):
        """Connect to the server."""
        # Get the user information
        user_name = self.get_user_name()
        password = self.get_password()

        # Create the client socket
        self.create_socket()

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
