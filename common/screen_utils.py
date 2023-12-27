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

    # Fix: Diana, arregla este inglés
    # Ask a number to the user
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
