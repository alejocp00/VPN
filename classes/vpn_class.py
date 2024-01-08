import threading
from classes.socket_manager import SocketManager
from classes.common.protocols.my_socket import MySocket
from classes.common.common_variables import *
from classes.common.screen_utils import *
from classes.log_manager import LogManager
from classes.threads_manager import ThreadManager
from classes.database.usersDb import *
from classes.database.vlansDb import *
from classes.database.ipDb import *
from classes.database.iprange import *
from classes.database.vlansIprangeDb import *
from classes.database.usersIprangeDb import *
from classes.vlan import Vlan
from classes.user import User


class MyVPN:
    def __init__(self):
        # Todo: Add the code to initialize the class
        self.protocol = VPNProtocol.UNKNOWN
        self.port = VPN_SERVER_PORT
        self.ip = VPN_SERVER_IP
        self.__process_flags = {}
        self.__thread_manager = ThreadManager()
        self.__socket_manager = SocketManager()
        self.__log_manager = LogManager()
        self.__vpn_status = VPNStatus.IDLE

    def __create_socket(self):
        "This method create the vpn server socket"
        self.__socket = MySocket(self.protocol)

    def __activate_socket(self):
        "This method activate the vpn server socket, and bind it to an specific address"
        self.__socket.bind((self.ip, self.port))

        if self.protocol == VPNProtocol.TCP:
            self.__socket.listen()

    def __run_server(self):
        "This method create a thread with the server process attached to it"
        if self.protocol == VPNProtocol.TCP:
            server_thread = threading.Thread(target=self.__tcp_server_process)
        else:
            server_thread = threading.Thread(target=self.__udp_server_process)

        server_thread.start()
        self.__thread_manager.add_thread(server_thread, "server")

    # def __create_fake_socket(self, client_address, ip_server, port_server):
    #     "This method create a fake socket for the client"

    #     # Create a fake socket
    #     fake_socket = MySocket(self.protocol)

    #     # Get the fake ip and port

    #     fake_ip = self.__extract_fake_ip(client_address)

    #     # Bind the fake socket to the fake ip and port

    #     fake_socket.bind((fake_ip, 0))  # 0 means auto assign port

    #     # Connect the fake socket to the server

    #     if self.protocol == VPNProtocol.TCP:
    #         fake_socket.connect((ip_server, port_server))

    #     # Return the fake socket

    #     return fake_socket

    def __extract_fake_ip(self, client_username):
        "This method extract the client fake ip"
        return get_assigned_ip_by_name(client_username)

    def __process_data(self, data, protocol: VPNProtocol, client_address):
        "This method process the data received from the client"
        if data is None:
            return

        # Check if the data is a login request
        if data[0] == REQUEST_LOGIN_HEADER:
            # Check if the user is valid
            if self.__is_valid_user(data[1], data[2]):
                # Send the response to the client with the ip assigned
                # Get the ip assigned to the user

                ip = get_assigned_ip_by_name(data[1])

                # Create the response message
                msg = self.__accepted_login_response(ip, protocol)

                # Send the response
                if protocol == VPNProtocol.UDP:
                    # Todo: change to the correct socket
                    response_socket = MySocket(VPNProtocol.UDP)
                    response_socket.connect(client_address)
                    self.__socket_manager.add_socket(response_socket, client_address)
                    response_socket.send(msg.encode())
                    print(msg)
                    print(client_address)
                else:
                    self.__socket_manager.get_socket_by_name(client_address).send(
                        msg.encode()
                    )

        elif data[0] == REQUEST_PACKAGE_HEADER:
            # Get the ip and port of the server
            ip_server = data[1]
            port_server = int(data[2])
            # Get the data to send
            data_to_send = data[3]
            # Create a socket to connect to the server
            temp_socket = MySocket(protocol)
            # Connect the socket to the server
            temp_socket.connect((ip_server, port_server))
            # Send the data to the server
            temp_socket.send(data_to_send.encode())
            adr = temp_socket.getsockname()
            self.__socket_manager.add_socket(temp_socket, client_address)
            # if protocol == VPNProtocol.UDP:
            #     temp_socket = MySocket(VPNProtocol.UDP)
            #     temp_socket.bind(adr)
            # Receive the response from the server
            response = temp_socket.recv(1024)
            if(protocol==VPNProtocol.UDP):
                response=response[0]
            # Process the response
            decoded_response = self.__decode_data(response)
            self.__process_data(decoded_response, protocol, client_address)

        elif data[0] == REQUEST_RESPONSE_HEADER:
            msg=";".join(data).encode()

            # Send the response to the client
            if(protocol==VPNProtocol.UDP):
                socket=MySocket(VPNProtocol.UDP)
                socket.bind(("localhost",0))
                socket.connect(client_address)
                socket.send(msg)
            else:
                self.__socket_manager.get_socket_by_name(client_address).send(msg)
            

    def __accepted_login_response(self, ip: str, protocol: VPNProtocol):
        "This method create the response message for a login request"
        response = REQUEST_ACCEPTED_HEADER + REQUEST_SEPARATOR + ip + REQUEST_SEPARATOR
        response += "tcp" if protocol == VPNProtocol.TCP else "udp"

        return response

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

        self.menu()

    #########
    #  TCP  #
    #########

    def __tcp_server_process(self):
        "This method is the main process of the server, it will be running until the server is stopped"
        while self.__vpn_status == VPNStatus.RUNNING:
            # Accept a connection
            client_socket, client_address = self.__socket.accept()

            # Add the socket to the socket manager
            self.__socket_manager.add_socket(client_socket, client_address)

            # Add to log
            self.__log_manager.add_log("New connection from: " + str(client_address))

            # Create a thread to handle the client
            client_thread = threading.Thread(
                target=self.__tcp_client_process, args=(client_socket, client_address)
            )
            client_thread.start()

            # Add the thread to the thread manager
            self.__thread_manager.add_thread(
                client_thread, "tcp_client_" + str(client_address)
            )

    def __tcp_client_process(self, client_socket, client_address):
        "This method is the main process of the client, it will be running until the client is disconnected"

        while self.__vpn_status == VPNStatus.RUNNING:
            # Receive the data
            data = client_socket.recv(1024)

            # If the client is disconnected
            if not data:
                break

            # Process the data
            decoded_data = self.__decode_data(data)
            if not decoded_data:
                break
            self.__process_data(decoded_data, VPNProtocol.TCP, client_address)

        # Close the socket
        client_socket.close()

        # Add to log
        self.__log_manager.add_log("Connection closed with: " + str(client_address))

        # Remove the socket from the socket manager
        self.__socket_manager.remove_socket(client_socket)

        # Remove the thread from the thread manager
        self.__thread_manager.remove_thread(threading.current_thread())

    #########
    #  UDP  #
    #########

    def __udp_server_process(self):
        "This method is the main process of the server, it will be running until the server is stopped"
        while self.__vpn_status == VPNStatus.RUNNING:
            recv_data, client_address = self.__socket.recv(1024)

            # Add to log
            self.__log_manager.add_log("Data received from: " + str(client_address))

            # Create a thread to handle the client
            client_thread = threading.Thread(
                target=self.__udp_client_process, args=[recv_data, client_address]
            )
            client_thread.start()

            # Add the thread to the thread manager
            self.__thread_manager.add_thread(client_thread, "client")

    def __udp_client_process(self, data, client_address):
        "This method is the main process of the client, it will be running until the client is disconnected"

        # Receive the data
        decoded_data = self.__decode_data(data)
        print(decoded_data)
        print(client_address)
        # Process the data
        self.__process_data(decoded_data, VPNProtocol.UDP, client_address)

        # Remove the thread from the thread manager
        self.__thread_manager.remove_thread(threading.current_thread())

    def __decode_data(self, data):
        "This method decode the data received from the client"


        split_data = data.decode().split(REQUEST_SEPARATOR)

        if not split_data:
            return None

        # Get login request
        if split_data[0] == REQUEST_LOGIN_HEADER:
            usr = split_data[1]
            pwd = split_data[2]
            print(usr)
            print(pwd)
            return (REQUEST_LOGIN_HEADER, usr, pwd)

        # Get normal request
        if split_data[0] == REQUEST_PACKAGE_HEADER:
            ip_server = split_data[1]
            port_server = split_data[2]
            data_to_send = split_data[3]
            return (REQUEST_PACKAGE_HEADER, ip_server, port_server, data_to_send)

        # Get server response
        if split_data[0] == REQUEST_RESPONSE_HEADER:
            response = split_data[1]
            return (REQUEST_RESPONSE_HEADER, response)

    #########
    # MENUS #
    #########

    def menu(self):
        """Show the menu."""
        # Todo: VPN menu as while true

        clear_screen()

        print("VPN Server")
        print(
            "Current state: {}".format(
                "Running" if self.__vpn_status == VPNStatus.RUNNING else "Stopped"
            )
        )
        print("Current protocol: {}".format(self.protocol))
        print("Current port: {}".format(self.port))
        print("Current IP: {}".format(self.ip))
        print("--------------------")

        options = [
            "1. Start server",
            "2. Create a client",
            "3. Create VLAN",
            "4. Restrict VLAN",
            "5. Restrict User",
            "6. Show log",
            "7. Stop server",
        ]

        print("\n".join(options))

        selected_option = input("Option: ")

        while selected_option not in [str(i) for i in range(1, len(options) + 1)]:
            self.menu()

        if selected_option == "1":
            if self.__vpn_status == VPNStatus.RUNNING:
                self.menu()
            self.__start_server_menu()
        elif selected_option == "2":
            self.__create_client_menu()
        elif selected_option == "3":
            self.__create_vlan_menu()
        elif selected_option == "4":
            self.__restrict_vlan_menu()
        elif selected_option == "5":
            self.__restrict_user_menu()
        elif selected_option == "6":
            self.__show_log()
        elif selected_option == "7":
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
        self.protocol = VPNProtocol.TCP if selected_option == "1" else VPNProtocol.UDP

        # Create socket
        self.__create_socket()

        # Activate socket
        self.__activate_socket()

        self.__vpn_status = VPNStatus.RUNNING

        # Create process thread
        self.__run_server()

        # Set status

        return self.menu()

    def __create_client_menu(self):
        """Create a client."""

        # Get client data
        client_user_name = get_user_name()

        # verify if username already exists in database
        existing_user = exists_user(client_user_name)

        if existing_user:
            print("The username inserted already exists")
            self.__create_client_menu()

        client_password = get_password(True)

        # Get VLAN
        vlan = self.__get_vlan()

        user = User(client_user_name, client_password, vlan)
        assignedIp = select_no_active_ip_by_vlan(vlan)

        insert_user(user, assignedIp)

        self.menu()

    def __get_vlan(self):
        "Get the vlan inserted and verifies if it's a valid vlan"
        vlan_temporal = get_id()

        existingVlan = exists_vlan(vlan_temporal)

        if not existingVlan:
            print("The inserted Vlan does not exists in database")
            self.__get_vlan()

        isVlanFull = is_vlan_full(vlan_temporal)
        if isVlanFull:
            print("The inserted Vlan does not have capacity for a new user")
            self.__get_vlan()

        return vlan_temporal

    def __create_vlan_menu(self):
        "Creates a vlan"
        vlanId = get_id()

        if exists_vlan(vlanId):
            print("The inserted Vlan already exists.")
            self.__create_vlan_menu()

        vlanIpAddress = get_ip_address()
        vlanMask = get_mask()

        vlan = Vlan(vlanId, vlanIpAddress, vlanMask)
        insert_vlan(vlan)
        self.__insert_vlan_ips(vlan)
        self.menu()

    def __insert_vlan_ips(self, vlan):
        "This function inserts all the ips of the created vlan into the database"
        ips = vlan.get_all_ips()
        for ip in ips:
            insert_ip(str(ip), vlan.id)
        return

    def __restrict_vlan_menu(self):
        """Restrict VLAN."""

        # Todo: get a list with all the vlans and show it to the user enumerated

        # Get vlan info
        vlan_temporal = get_id()
        existingVlan = exists_vlan(vlan_temporal)

        if not existingVlan:
            print("The inserted Vlan does not exists in database")
            self.__restrict_vlan_menu()

        ipRange = get_ip_range()
        insert_ip_range(ipRange)
        ipRangeId = select_id_for_ip_range(ipRange)
        insert_vlan_ip_range(vlan_temporal, ipRangeId)

        self.menu()

    def __restrict_user_menu(self):
        """Restrict User."""

        # Get user id
        userId = get_id(True)
        existingUser = exists_user_by_id(userId)

        if not existingUser:
            print("The user id inserted does not exists in database")
            self.__restrict_user_menu()

        ipRange = get_ip_range()
        insert_ip_range(ipRange)
        ipRangeId = select_id_for_ip_range(ipRange)

        insert_user_ip_range(userId, ipRangeId)
        return self.menu()

    def __is_in_range(self, ip, ipRange):
        "This function verifies if an ip address is in a ip range"
        octantsRange = ipRange.split(".")
        octantsIp = ip.split(".")

        for i in range(0, len(octantsRange)):
            if octantsRange[i] == "x":
                return True
            if octantsRange[i] != octantsIp[i]:
                return False

        return True

    def __is_valid_user(self, username, password):
        existingUser = exists_user(username)
        if not existingUser:
            return False
        if password != select_user_password(username):
            return False
        return True
