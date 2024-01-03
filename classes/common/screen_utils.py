import ipaddress
import os


def clear_screen():
    """Clear the screen."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_user_name():
    """Get the user name."""

    clear_screen()

    user_name = input("User name: ")

    # Check if the user name is valid
    if not user_name:
        print("The user name is required.")
        return get_user_name()

    # Check if the user name was correctly entered
    if "y" != input(f"Is {user_name} correct? (y/n): "):
        return get_user_name()

    return user_name


def get_password(repeat=False):
    """Get the password."""

    clear_screen()

    password = input("Password: ")

    if repeat:
        password2 = input("Type password again: ")
        if password != password2:
            input("Password are different. Press any key to type again")
            get_password(True)

    # Check if the password is valid
    if not password:
        print("The password is required.")
        return get_password()

    return password


def get_id(isUser=False):
    """Ask the user for a VLAN or User ID"""

    clear_screen()
    objective = "user" if isUser else "VLAN"

    # Ask the user for a number
    number = input(f"Enter the {objective} id: ")

    if not number.isnumeric():
        get_id()

    return int(number)


def get_ip_range():
    """Ask a ip range to the user"""

    clear_screen()

    ip_range = input("Enter a valid ip range: ")

    if not ip_range or ip_range == "":
        get_ip_range()

    # Check if the range is valid
    octants = ip_range.split(".")

    if octants.count != 4:
        get_ip_range()

    for octant in octants:
        # Check if all chars of the octant are numbers
        if octant.isnumeric():
            for c in octant:
                if not c.isnumeric():
                    get_ip_range()
            # Check if it is 0<=x<256
            if int(octant) < 0 or int(octant) > 255:
                get_ip_range()

        # Check if the octant have an x
        elif not octant.lower() == "x":
            get_ip_range()

    return ip_range

def validate_ip_address(ip):
   "This function verifies if the input is a valid ip address"
   try:
       ip_object = ipaddress.ip_address(ip)
       return True
   except ValueError:
       return False
   
def validate_mask(mask):
    "This function verifies if the input is a valid mask"
    # ToDo: implementar validacion de la mascara que pasa el usuario
    pass

def get_ip_address():
    "Ask user for the vlan ip address"
    ip_address = input("Enter a valid ip address: ")

    if not validate_ip_address(ip_address):
        print("The value inserted is not a valid ip address")
        get_ip_address()

    return ip_address

def get_mask():
    "Ask user for the vlan mask"
    mask = input("Enter a valid mask:")

    #habria que validar la mask
    return mask