import os


def clear_screen():
    """Clear the screen."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
