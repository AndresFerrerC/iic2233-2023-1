from __future__ import annotations
from parametros import VOLVER, SALIR
from torneo import Torneo
import flujo_torneo as flujo
import manejo_txt


def menu_inicio_print_opciones() -> None:
    """Realiza un print del menú de inicio"""
    texto_menu = "   *** Menú de Inicio ***   \n" \
        "[1] Nueva partida\n" \
        "[2] Cargar partida\n" \
        "[X] Salir"
    print(texto_menu)


def menu_principal_print_opciones(dia: int, total_dias: int,
                                  tipo_arena: int) -> None:
    """Realiza un print del menú principal"""
    texto_menu = "   *** Menú Principal ***   \n" \
        f"Día torneo DCCavaCava: {dia}/{total_dias}\n" \
        f"Tipo de arena: {tipo_arena}\n" \
        "[1] Simular día torneo\n" \
        "[2] Ver estado torneo\n" \
        "[3] Ver ítems\n" \
        "[4] Guardar partida\n" \
        "[5] Volver\n" \
        "[X] Salir del programa"
    print(texto_menu)


def cargar_partida_archivo(archivo: str) -> Torneo:
    """Devuelve una partida instanciada con
    todos los excavadores, ítems y demás
    datos extraídos de una partida guardada"""
    items = []
    excavadores = []
    partida = flujo.cargar_partida_vacia()
    path = manejo_txt.path_destino(archivo)
    with open(path, "rt", encoding="utf8") as f:
        for linea in f:
            contenido = linea.rstrip()
            separador = contenido.split(";")
            if len(separador) == 2:  # válido
                tipo = separador[0]
                datos = separador[1].split(",")

                # Instanciar un consumible
                if tipo == "CONSUMIBLE":
                    consumible = flujo.instanciar_consumible(datos)
                    items.append(consumible)

                # Instanciar un tesoro
                elif tipo == "TESORO":
                    tesoro = flujo.instanciar_tesoro(datos)
                    items.append(tesoro)

                # Instanciar un excavador
                elif tipo == "EXCAVADOR":
                    excavador = flujo.cargar_excavador(datos)
                    excavadores.append(excavador)

                # Carga de la arena (única)
                elif tipo == "ARENA":
                    tipo, nombre = datos[0], datos[1]
                    rareza, humedad = int(datos[2]), int(datos[3])
                    dureza, estatica = int(datos[4]), int(datos[5])
                    dificultad = float(datos[6])
                    caracteristicas = [nombre, tipo, rareza, humedad, 
                                       dureza, estatica]
                    arena = flujo.instanciar_arena(tipo, caracteristicas)
                    arena.dificultad = dificultad
                    partida.arena_actual = arena

                # Carga de datos del torneo (únicos)
                elif tipo == "TORNEO":
                    meta, total_cavado = float(datos[0]), float(datos[1])
                    dias_transcurridos = int(datos[2])
                    dias_totales = int(datos[3])
                    partida.meta = meta
                    partida.metros_cavados = total_cavado
                    partida.dias_transcurridos = dias_transcurridos
                    partida.dias_totales = dias_totales
    # Asignar excavadores e ítems instanciados en la partida
    partida.equipo_excavadores = excavadores
    partida.mochila_items = items
    return partida


def menu_carga() -> list:
    """Inicializa el menú de carga.
    Formato: [respuesta, partida instanciada]"""
    opciones = manejo_txt.opciones_partida()
    while True:
        print("*** Menú de carga ***\n" + "-" * 30)
        numero = 1
        if len(opciones) > 0:
            for opcion in opciones:
                print(f"[{numero}] {opcion}")
                numero += 1
        else:
            print("No hay archivos para cargar :(".center(30))
            print("*** Intente nuevamente ***")
            return [SALIR, None]
        print("-" * 30)
        lista_opciones = [str(n + 1) for n in range(numero - 1)]
        print("[X] Salir del programa")
        input_comas = (', ').join(lista_opciones)
        resp = input(f"Indique su opción ({input_comas} o X): ")
        if resp in lista_opciones:
            archivo = opciones[int(resp) - 1]
            partida = cargar_partida_archivo(archivo)
            return ["ir_menu_principal", partida]
        elif resp == "x" or resp == "X":
            return [SALIR, None]


def menu_inicio() -> None:
    """Inicializa el menú de inicio"""
    while True:
        menu_inicio_print_opciones()
        resp = input("Indique su opción (1, 2 o X): ")
        if resp == "1":
            return "ir_menu_principal"
        elif resp == "2":
            return "ir_menu_carga"
        elif resp == "X" or resp == 'x':
            return SALIR


def menu_principal(partida: Torneo):
    """Inicializa el menú principal"""
    while True:
        dias, totales = partida.dias_transcurridos, partida.dias_totales
        tipo_arena = partida.arena_actual.tipo
        menu_principal_print_opciones(dias, totales, tipo_arena)
        resp = input("Indique su opción (1, 2, 3, 4, 5 o X): ")
        if resp == "1":
            return partida.simular_dia()
        elif resp == "2":
            partida.mostrar_estado()
            # No hay return para volver a mostrar el menú
        elif resp == "3":
            return "ir_menu_items"
        elif resp == "4":
            print("*** Guardar partida ***")
            print("A continuación, ingrese el nombre del archivo a guardar"
                  " en la carpeta Partidas. \n * NO incluya una extensión. *")
            destino = input("Ingrese el nombre del archivo a guardar: ")
            guardado = manejo_txt.guardar_partida(partida, destino)
            print(f"La partida ha sido guardada exitosamente en {guardado}.")
        elif resp == "5":
            return VOLVER
        elif resp == "X" or resp == 'x':
            return SALIR


def mostrar_menu_items(partida: Torneo, lista_items: list) -> None:
    """Imprime el menú con ítems disponibles."""
    while True:
        print("*** Menú Ítems ***".center(75) + "\n" + "-" * 80)
        columna_1, columna_2, columna_3 = "Nombre", "Tipo", "Descripción"
        print(f"{columna_1:33.33s}  | {columna_2:10.10s} | {columna_3:65.65s}")
        print("-" * 80)
        numero = 1
        # Print de los ítems disponibles y su opción
        if len(lista_items) > 0:
            for item in lista_items:
                nombre, tipo, descripcion = item.nombre, item.tipo, \
                    item.descripcion
                print(f"[{numero}] {nombre:30.30s} | {tipo:10.10s} |"
                      f" {descripcion:65.65s}")
                numero += 1
        else:
            print("No hay :(".center(80))

        print("-" * 80)
        print(f"[{numero}] Volver")
        print("[X] Salir del programa")
        lista_opciones = [str(n + 1) for n in range(numero - 1)]
        if len(lista_opciones) > 0:
            input_comas = (', ').join(lista_opciones) + f", {numero}"
        else:
            input_comas = "1"
        resp = input(f"Indique su opción ({input_comas} o X): ")

        if resp in lista_opciones:
            elemento = lista_items[int(resp) - 1]
            if elemento.tipo == "consumible":
                partida.usar_consumible(elemento)
            else:
                partida.abrir_tesoro(elemento)
            # Remoción del ítem de la mochila de la clase instanciada
            lista_items.remove(elemento)
        elif resp == str(numero):
            return VOLVER
        elif resp == "x" or resp == "X":
            return SALIR


def imprimir_estado_torneo(dia: int, tipo: str, nombre: str,
                           dificultad: float, metros: float,
                           meta: float, excavadores: list) -> None:
    """Imprime el estado del torneo."""
    print("*** Estado Torneo ***".center(75) + "\n" + "-" * 80)
    print(f"Día actual: {dia}")
    print(f"Tipo de arena: {tipo} de nombre {nombre} [Dificultad: "
          f"{dificultad}]")
    print(f"Metros excavados: {metros}/{meta}")
    columna_1, columna_2, columna_3 = "Nombre", "Edad", "Tipo"
    columna_4, columna_5, columna_6 = "Energía", "Fuerza", "Suerte"
    columna_7 = "Felicidad"
    print("-" * 80 + "\n" + "Excavadores".center(75) + "\n" + "-" * 80)
    print(f"{columna_1:15.15s} | {columna_2:4.4s} | {columna_3:10.10s} | "
          f"{columna_4:7.7s} | {columna_5:7.7s} | {columna_6:7.7s} |"
          f" {columna_7:10.10s}")
    print("-" * 80)
    for excavador in excavadores:
        edad = excavador.edad
        nombre, tipo = excavador.nombre, excavador.tipo
        energia, fuerza = excavador.energia, excavador.fuerza
        suerte, felicidad = excavador.suerte, excavador.felicidad
        print(f"{nombre:15.15s} | {edad:^4d} | {tipo:10.10s} | {energia:^7d}"
              f" | {fuerza:^7d} | {suerte:^7d} | {felicidad:^10d}")
    print("-" * 80)


def menu_manager():
    """Inicializa el flujo de los menú"""
    historial = ["ir_menu_inicio"]
    respuesta = ""
    partida = None
    while respuesta != SALIR:
        estado_actual = historial[-1]

        if estado_actual == "ir_menu_inicio":
            partida = flujo.nueva_partida()
            respuesta = menu_inicio()
            
        elif estado_actual == "ir_menu_principal":
            respuesta = menu_principal(partida)

        elif estado_actual == "ir_menu_items":
            lista = partida.ver_mochila()
            respuesta = mostrar_menu_items(partida, lista)

        elif estado_actual == "ir_menu_carga":
            estado_preliminar = menu_carga()  # [respuesta, partida]
            partida = estado_preliminar[1]
            respuesta = estado_preliminar[0]

        if respuesta == VOLVER:
            historial.pop()

        elif respuesta.startswith("ir"):
            if respuesta != estado_actual:
                historial.append(respuesta)
