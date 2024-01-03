from classes.client import Client
from classes.common.screen_utils import clear_screen


class SumClient(Client):
    def __init__(self):
        super().__init__()

    def execute_function(self):
        """Execute the function."""
        # Get the numbers
        num1 = self.__get_number()
        num2 = self.__get_number()

        data = f"{num1},{num2}"

        print("Sending the numbers to the server...")

        # Send the numbers to the server
        self._socket.send(data.encode())

        print("Waiting for the result...")
        # Receive the result
        result = self._socket.recv(1024).decode()

        # Print the result
        print(f"The result is: {result}")

    def __get_number(self):
        """Get a number from the user."""
        while True:
            clear_screen()
            try:
                number = int(input("Enter a number: "))
                break
            except ValueError:
                print("Please enter a valid number")

        return number
