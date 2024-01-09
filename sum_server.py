from classes.server import Server


class SumServer(Server):
    def __init__(self, server_ip):
        super().__init__(server_ip)

    def _server_function(self, data, client_socket, client_address) -> str:
        # Get the numbers
        num1, num2 = data.split(",")

        # Sum the numbers
        result = int(num1) + int(num2)

        # Return the result
        return str(result)


SumServer("localhost").menu()
