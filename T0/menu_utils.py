import os
import functions
import tablero


def obtener_archivo_inicio() -> str:
    """ Obtiene la ruta del archivo """
    print("*** Menú de Inicio ***")
    nombre_archivo = input("Indique el nombre del archivo que desea abrir: ")
    return nombre_archivo


def entregar_ruta(direccion: str) -> str:
    """Entrega la ruta corregida con os"""
    nombre = os.path.basename(direccion)
    ruta = os.path.join("Archivos", nombre)
    return ruta


def existe_archivo(archivo: str) -> bool:
    """Devuelve True si existe el archivo"""
    return os.path.isfile(entregar_ruta(archivo))


def menu_acciones_print_opciones() -> None:
    """Imprime el menú de acciones. Es solo un print para el usuario
     y sirve para no dificultar la lectura del flujo del menú en sí"""
    string_opciones = "*** Menu de Acciones ***\n" \
        " [1] Mostrar tablero\n" \
        " [2] Validar tablero\n" \
        " [3] Revisar solución\n" \
        " [4] Solucionar tablero\n" \
        " [5] Salir del programa"
    print(string_opciones)


def menu_acciones(archivo: str) -> None:
    """ Segundo menú ejecutable. Flujo principal """
    menu_acciones_print_opciones()  # ejecución menú
    opcion_menu = input("Indique su opción (1, 2, 3, 4 o 5): ")
    opciones_str = ["1", "2", "3", "4", "5"]
    while opcion_menu not in opciones_str:
        menu_acciones_print_opciones()
        print("* -> Recuerda ingresar una de las opciones adecuadas :3")
        opcion_menu = input("Indique su opción (1, 2, 3, 4 o 5): ")
    opcion_menu = int(opcion_menu)  # conversión
    ejecutar_acciones(opcion_menu, archivo)


def validar_bombas_tortugas(tablero: list) -> None:
    """Verifica cumplimiento de reglas 2, 4 y 5"""
    regla_2 = functions.verificar_valor_bombas(tablero) == 0
    regla_4 = functions.verificar_tortugas(tablero) == 0
    regla_5 = functions.verificar_islas(tablero) is False
    if regla_2 and regla_4 and regla_5:
        print("* ¡El tablero es válido para las reglas 2, 4 y 5! :D")
    else:
        print("* D: El tablero NO es válido para las reglas 2, 4 y 5 :-(")


def validar_solucion(tablero: list) -> None:
    """Verifica cumplimiento de reglas 1, 2, 3, 4 y 5"""
    if functions.cumple_reglas(tablero):
        print("* :D ¡Yay! El tablero es válido y está resuelto owo/")
    else:
        print("* D: El tablero no cumple con todas las reglas UnU'")


def advertir_solucion_tablero(lista_tablero: list) -> bool:
    """Devuelve True si es que se puede llamar a la función
    buscar solución"""
    if functions.cumple_reglas(lista_tablero):  # ya está solucionado.
        print("* :/ El tablero ya cumple con todas las reglas, está listo.")
        print("* -> Sin embargo, a continuación lo puedes visualizar: ")
        tablero.imprimir_tablero(lista_tablero)
        return False
    if len(lista_tablero) > 4:
        advertencia_str = "* ! -> El tablero es algo grande. Su resolución" \
                " puede tardar varios minutos. \n* ... Buscando solución ..."
        print(advertencia_str)
    return True


def obtener_solucion_tablero(lista_tablero: list, ruta: str) -> None:
    if advertir_solucion_tablero(lista_tablero):
        solucionado = functions.solucionar_tablero(lista_tablero)
        if solucionado is not None:
            print("* El tablero ha sido solucionado owo/")
            print("* -> Tablero solucionado a continuación:")
            nombre_separado = os.path.splitext(ruta)
            destino = nombre_separado[0] + "_sol" + nombre_separado[1]
            functions.guardar_tablero(destino, solucionado)
            tablero.imprimir_tablero(solucionado)
            print(f"El tablero se ha guardado en {destino}.")
        else:
            print("* D: El tablero no se pudo solucionar :'c")


def ejecutar_acciones(opcion: int, archivo: str) -> None:
    lista_tablero = functions.cargar_tablero(entregar_ruta(archivo))
    if opcion == 1:
        tablero.imprimir_tablero(lista_tablero)
        menu_acciones(entregar_ruta(archivo))
    elif opcion == 2:
        validar_bombas_tortugas(lista_tablero)
        menu_acciones(entregar_ruta(archivo))
    elif opcion == 3:
        validar_solucion(lista_tablero)
        menu_acciones(entregar_ruta(archivo))
    elif opcion == 4:
        obtener_solucion_tablero(lista_tablero, entregar_ruta(archivo))
        menu_acciones(entregar_ruta(archivo))
    return  # cerrar en caso de la otra opción (5)
