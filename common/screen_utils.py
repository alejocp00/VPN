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
