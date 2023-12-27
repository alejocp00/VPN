from common.common_variables import *
from common.protocols.my_socket import MySocket
from common.screen_utils import *


class MyVPN:
    def __init__(self):
        # Todo: Add the code to initialize the class
        self.is_running = False
        self.protocol = VPNProtocol.UNKNOWN
        self.port = VPN_SERVER_PORT
        self.ip = VPN_SERVER_IP
        self.__socket = None
        self.process_flags = {
            "log": False,
        }
        pass

    def __create_socket(self):
        "This method create the vpn server socket"
        # Todo: Implement create socket
        pass

    def __activate_socket(self):
        "This method activate the vpn server socket, and bind it to an specific address"
        # Todo: Implement activate socket
        pass

    def __run_server(self):
        "This method create a thread with the server process attached to it"
        # Todo: implement run server
        pass

    def __show_log(self):
        """Show the log."""
        # Todo: Add the code to show the log
        pass

    def __stop_server(self):
        """Stop the server."""
        # Todo: Add the code to stop the server
        pass

    #########
    # MENUS #
    #########

    def menu(self):
        """Show the menu."""

        clear_screen()

        print("VPN Server")
        print("Current state: {}".format("Running" if self.is_running else "Stopped"))
        print("Current protocol: {}".format(self.protocol))
        print("Current port: {}".format(self.port))
        print("Current IP: {}".format(self.ip))
        print("--------------------")

        options = [
            "1. Start server",
            "2. Create a client",
            "3. Restrict VLAN",
            "4. Restrict User",
            "5. Show log" "6. Stop server",
            "6. Stop server",
        ]

        print("\n".join(options))

        selected_option = input("Option: ")

        while selected_option not in [str(i) for i in range(1, len(options) + 1)]:
            self.menu()

        if selected_option == "1":
            self.__start_server_menu()
        elif selected_option == "2":
            self.__create_client_menu()
        elif selected_option == "3":
            self.__restrict_vlan_menu()
        elif selected_option == "4":
            self.__restrict_user_menu()
        elif selected_option == "5":
            self.__show_log()
        elif selected_option == "6":
            self.__stop_server()
        else:
            self.menu()

    def __start_server_menu(self):
        """Start the server."""

        # Options to select
        options = ["1. use_tcp", "2. use_udp"]

        # Cleaning the screen
        clear_screen()

        # Showing select text
        print("Select a protocol to use.")

        # Printing options
        print("\n".join(options))

        selected_option = input("Option: ")

        # Capture back option
        if selected_option == "b":
            self.menu()

        if selected_option not in [str(i) for i in range(1, len(options) + 1)]:
            self.__start_server_menu()

        # Update protocol server
        self.protocol = VPNProtocol.TCP if selected_option == 1 else VPNProtocol.UDP

        # Create socket
        self.__create_socket()

        # Activate socket
        self.__activate_socket()

        # Create process thread
        self.__run_server()

    def __create_client_menu(self):
        """Create a client."""
        # Todo: Add the code to create a client
        pass

    def __restrict_vlan_menu(self):
        """Restrict VLAN."""
        # Todo: Add the code to restrict VLAN
        pass

    def __restrict_user_menu(self):
        """Restrict User."""
        # Todo: Add the code to restrict User
        pass
