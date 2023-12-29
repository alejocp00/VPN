import socket
import threading
from common.common_variables import *
from common.protocols.my_socket import MySocket
from common.protocols.my_tcp import MyTCP
from common.protocols.my_udp import MyUDP
from common.screen_utils import *
from vpn.src.classes.log_manager import LogManager
from vpn.src.classes.socket_manager import SocketManager
from vpn.src.classes.threads_manager import ThreadManager


class MyVPN:
    def __init__(self):
        # Todo: Add the code to initialize the class
        self.is_running = False
        self.protocol = VPNProtocol.UNKNOWN
        self.port = VPN_SERVER_PORT
        self.ip = VPN_SERVER_IP
        self.__socket = None
        self.__process_flags = {}
        self.__thread_manager = ThreadManager()
        self.__socket_manager = SocketManager()
        self.__log_manager = LogManager()
        self.__vpn_status = VPNStatus.IDLE

    def __create_socket(self):
        "This method create the vpn server socket"
        # Todo: Correctly implement create socket
        if self.protocol == VPNProtocol.TCP:
            self.__socket = MyTCP()
        elif self.protocol == VPNProtocol.UDP:
            self.__socket = MyUDP()
        else:
            raise Exception("Protocol not supported")

    def __activate_socket(self):
        "This method activate the vpn server socket, and bind it to an specific address"
        # Todo: Correctly implement activate socket
        pass

    def __run_server(self):
        "This method create a thread with the server process attached to it"
        # Todo: Correctly implement run server
        server_thread = threading.Thread(target=self.__server_process)
        server_thread.start()
        self.__thread_manager.add_thread(server_thread, "server")

    def __server_process(self):
        "This method is the main process of the server, it will be running until the server is stopped"
        # Todo: Correctly implement server process
        # while self.__vpn_status == VPNStatus.RUNNING:
        #     # Accept a connection
        #     client_socket, client_address = self.__socket.accept()

        #     # Add the socket to the socket manager
        #     self.__socket_manager.add_socket(client_socket, client_address)

        #     # Add to log
        #     self.__log_manager.add_log("New connection from: " + str(client_address))

        #     # Create a thread to handle the client
        #     client_thread = threading.Thread(
        #         target=self.__client_process, args=(client_socket, client_address)
        #     )
        #     client_thread.start()

        #     # Add the thread to the thread manager
        #     self.__thread_manager.add_thread(client_thread)
        pass

    def __client_process(self, client_socket, client_address):
        "This method is the main process of the client, it will be running until the client is disconnected"
        # Todo: Correctly implement client process
        # while self.__vpn_status == VPNStatus.RUNNING:
        #     # Receive the data
        #     data = client_socket.recv(1024)

        #     # If the client is disconnected
        #     if not data:
        #         break

        #     # Process the data
        #     self.__process_data(data)

        # # Close the socket
        # client_socket.close()

        # # Remove the socket from the socket manager
        # self.__socket_manager.remove_socket(client_socket)

        # # Remove the thread from the thread manager
        # self.__thread_manager.remove_thread(threading.current_thread())
        pass

    def __process_data(self, data):
        "This method process the data received from the client"
        # Todo: Is this necessary?
        pass

    def __show_log(self):
        """Show the log."""

        clear_screen()

        stop_flag = False

        # Log tex print process
        def print_text():
            while not stop_flag:
                if self.__log_manager.new_logs():
                    clear_screen()
                    print(self.__log_manager.get_logs())

        # Create the thread
        print_thread = threading.Thread(target=print_text)
        print_thread.start()

        # Wait for the back signal
        while input() != "b":
            continue

        stop_flag = True

        print_thread.join()

        return self.menu()

    def __stop_server(self):
        """Stop the server."""

        # Set the vpn status
        self.__vpn_status = VPNStatus.SHUTING_DOWN

        # Close all sockets
        self.__socket_manager.clear()

        # Close Threads
        self.__thread_manager.dying_light(True)

        self.__vpn_status = VPNStatus.IDLE

        self.menu

    #########
    # MENUS #
    #########

    def menu(self):
        """Show the menu."""
        # Todo: VPN menu as while true

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
            "5. Show log",
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

        # Set status
        self.__vpn_status = VPNStatus.RUNNING

    def __create_client_menu(self):
        """Create a client."""

        # Get client data
        client_user_name = get_user_name()
        client_password = get_password()

        # Get VLAN
        vlan_temporal = get_id

        # Todo: Check for vlan, and user

        # Todo: Add user to the database

        self.menu()

    def __restrict_vlan_menu(self):
        """Restrict VLAN."""

        # Get vlan info
        vlan_temporal = get_id()

        # Todo:  check if vlan exist
        ip_range = get_ip_range()

        # Todo: Add to database

        self.menu()

    def __restrict_user_menu(self):
        """Restrict User."""

        # Get user id
        user_id = get_id(True)

        # Todo: Check if user id is correct

        # Get vlan id
        vlan_id = get_id(False)

        # Todo: Check if vlan id is correct

        # Todo: Add it to database

        return self.menu()
