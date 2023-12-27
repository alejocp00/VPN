from common.common_variables import *
from common.screen_utils import *


class MyVPN:
    def __init__(self):
        # Todo: Add the code to initialize the class
        self.is_running = False
        self.protocol = VPNProtocol.UNKNOWN
        self.port = None
        self.ip = None
        pass

    def __start_server(self):
        """Start the server."""
        # Todo: Add the code to start the server
        pass

    def __create_client(self):
        """Create a client."""
        # Todo: Add the code to create a client

        pass

    def __restrict_vlan(self):
        """Restrict VLAN."""
        # Todo: Add the code to restrict VLAN
        pass

    def __restrict_user(self):
        """Restrict User."""
        # Todo: Add the code to restrict User
        pass

    def __show_log(self):
        """Show the log."""
        # Todo: Add the code to show the log
        pass

    def __stop_server(self):
        """Stop the server."""
        # Todo: Add the code to stop the server
        pass

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
            clear_screen()
            self.menu()

        if selected_option == "1":
            self.__start_server()
        elif selected_option == "2":
            self.__create_client()
        elif selected_option == "3":
            self.__restrict_vlan()
        elif selected_option == "4":
            self.__restrict_user()
        elif selected_option == "5":
            self.__show_log()
        elif selected_option == "6":
            self.__stop_server()
        else:
            self.menu()
