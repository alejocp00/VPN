import socket
import threading
import Functions
import inspect
import os


def Menu():

    # Recopilando los nombres de los metodos de la clase Functions
    functions = Functions.Functions()
    method_names = []
    method_dict = {}

    for name, method in inspect.getmembers(functions, inspect.ismethod):
        if not name.startswith("__"):
            method_names.append(name)

    index = 1
    for name in method_names:
        method_dict[str(index)] = name
        index += 1

    while True:
        os.system('clear')
        print("Seleccione una Operacion:")

        # Imprimiendo las opciones del menu

        for index, name in method_dict.items():
            print(index, name)

        option = input("> ")
        os.system('clear')

        # Para llamar a la funcion correspondiente

        if option in method_dict:
            method_name = method_dict[option]
            method = getattr(functions, method_name)
            method()
        else:
            print("Opcion no valida")


if __name__ == "__main__":
    Menu()