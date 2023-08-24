import menu_utils as menu


def menu_inicio():
    archivo = menu.obtener_archivo_inicio()
    if menu.existe_archivo(archivo):
        menu.menu_acciones(archivo)
    else:
        print("El archivo no existe :(")


if __name__ == "__main__":
    menu_inicio()
