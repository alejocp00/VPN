from classes.client import Client
from classes.common.screen_utils import clear_screen


class SumClient(Client):
    def __init__(self):
        super().__init__()

    def execute_function(self, ip, port):
        """Execute the function."""
        msg = input("What do you want to say to the server? ")

        # Send the numbers to the server
        self._send_data(ip, port, msg)

        print("Waiting for the result...")
        # Receive the result
        result = self._receive_data()

        # Print the result
        print(f"Well, the server say: {result}")


SumClient().menu()
