from classes.server import Server


class SumServer(Server):
    def __init__(self, server_ip):
        super().__init__(server_ip)

    def _server_function(self, data, client_socket, client_address) -> str:
        # Get the numbers
        print("Hi, I'm the server. So you are telling me: " + data)
        response = "Chipi chipi chapa chapa dubi dubi daba daba mágico mi dubi dubi bum bum bum bum"
        print(
            "That's nice, but you know what? I don't care, and I tell you: " + response
        )
        # Return the result
        return response


SumServer("localhost").menu()
