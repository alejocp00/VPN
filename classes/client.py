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
        self.__perform_first_connection()

        # Connect to the server
        self._connect_to_server()

        self.menu()

    def _connect_to_server(self):
        """Connect to the server."""
        self.__socket = MySocket(self._config["protocol"])
        if self._config["protocol"] == VPNProtocol.UDP:
            self.__socket.bind(('127.0.0.2',0))
        else:
            self.__socket.bind(('127.0.0.2',17))
            self.__socket.connect((self._config["server_ip"], self._config["server_port"]))

    def __perform_first_connection(self):
        """Get the VPN protocol."""

        # Instance a new MyTCP socket for the first connection
        self.__socket = MySocket(VPNProtocol.TCP)
        using_udp = False
        # Create the request message
        request_message = self.__create_request_message()
        try:
            # Connect the socket to the server
            self.__socket.connect(
                (self._config["server_ip"], self._config["server_port"])
            )
        except:
            self.__socket.close()
            self.__socket = MySocket(VPNProtocol.UDP)
            self.__socket.bind(('127.0.0.2',0))#
            # self.__socket.connect(
            #     (self._config["server_ip"], self._config["server_port"])
            # )
            using_udp = True
        # Send the request message
        self.__socket.send(request_message,(self._config["server_ip"], self._config["server_port"]))
        if using_udp:
            adr = ('127.0.0.2',0)#self.__socket.getsockname()
            self.__socket = MySocket(VPNProtocol.UDP)
            self.__socket.bind(adr)
        # Receive the response message
        response_message = self.__socket.recv(1024)
        if using_udp:
            response_message = response_message[0]
            response_message=response_message.encode()
        
        response_message = response_message.decode()
        
        # Process the response
        self.__set_configuration(response_message)

        # Close
        self.__socket.close()

    def __create_request_message(self):
        """Create the request message."""
        message = ""

        # Indicate that is a login request
        message += REQUEST_LOGIN_HEADER + REQUEST_SEPARATOR

        # Add the user name
        message += self._user_name + REQUEST_SEPARATOR

        # Add the password
        message += str(self.__password)

        return message.encode()

    def __set_configuration(self, received_data):
        """Set the configuration."""

        if not received_data or received_data == "":
            
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
            
            raise Exception(f"Error: {received_data[1]}")

    def disconnect(self):
        """Disconnect from the server."""
        self.__socket.close()

    def _send_data(self, ip_server: str, port_server: int, data: str):
        """Send data to the server."""
        msg = (
            REQUEST_PACKAGE_HEADER
            + REQUEST_SEPARATOR
            + ip_server
            + REQUEST_SEPARATOR
            + str(port_server)
            + REQUEST_SEPARATOR
            + data
        )

        self.__socket.send(msg.encode(),(self._config["server_ip"], self._config["server_port"]))

    def _receive_data(self):
        """Receive data from the server."""
        if self._config["protocol"] == VPNProtocol.TCP:
            return self.decode_data(self.__socket.recv(1024).decode())

        adr = self.__socket.getsockname()
        self.__socket = MySocket(VPNProtocol.UDP)
        self.__socket.bind(adr)
        
        resp=self.__socket.recv(1024)[0]
        
        return self.decode_data(resp)

    def decode_data(self, data: str):
        """Decode the data received from the server."""
        splitted_data = data.split(REQUEST_SEPARATOR)

        if len(splitted_data) != 2:
            raise Exception("Error: The received data is not correct")

        return splitted_data[1]

    @abstractmethod
    def execute_function(self, ip, port):
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
            
            self.execute_function(get_ip_address(), input("port: "))
        elif option == "3":
            self.disconnect()
        else:
            self.menu()
