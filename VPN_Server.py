import socket
import threading
import Functions
import inspect
import os


def Menu():

    print("Seleccione una Operacion:")
    functions = Functions.Functions()
    index = 1
    for name, method in inspect.getmembers(functions, inspect.ismethod):
        if not name.startswith("__"):

            print(index, name)
            index += 1

    option = input("> ")

    # Limpiar pantalla
    
    os.system('clear')#Linux


    if option == "1":
        functions.start_server()

    elif option == "2":
        functions.create_user()

    elif option == "3":
        functions.login_user()
    
    elif option == "4":
        functions.restrict_vlan()

    elif option == "5":
        functions.restrict_user()

    elif option == "6":
        functions.log()

    elif option == "7":
        functions.stop()
    
    else:
        print("Opcion no valida")
        Menu()




if __name__ == "__main__":
    print("Bienvenido al servidor VPN")
    Menu()