from random import choices, sample
from parametros import CSV_ARENAS, CSV_CONSUMIBLES, \
    CSV_EXCAVADORES, CSV_TESOROS


def lista_arenas() -> list:
    """Entrega una lista de listas que contiene a las arenas"""
    lista_de_arenas = []
    with open(CSV_ARENAS, "rt", encoding="utf-8") as f:
        for linea in f:
            contenido = linea.strip()
            if not contenido.endswith("estatica"):
                contenido_arena = contenido.split(",")
                for i in range(2, 6):
                    contenido_arena[i] = int(contenido_arena[i])
                lista_de_arenas.append(contenido_arena)
    return lista_de_arenas


def obtener_arena(tipo: str) -> list:
    """Entrega una lista que contiene
    una arena del tipo (str) aleatoria"""
    arena_seleccionada = [[]]
    if tipo in ['magnetica', 'normal', 'rocosa', 'mojada']:
        posibles = [arena for arena in lista_arenas() if arena[1] == tipo]
        arena_seleccionada = choices(posibles, k=1)
    return arena_seleccionada[0]


# Excavadores

def lista_excavadores() -> list:
    """Entrega una lista de listas que
    contiene a los excavadores"""
    lista_de_excavadores = []
    with open(CSV_EXCAVADORES, "rt", encoding="utf-8") as f:
        for linea in f:
            contenido = linea.strip()
            if not contenido.endswith("felicidad"):
                contenido_excavador = contenido.split(",")
                for i in range(2, 7):
                    contenido_excavador[i] = int(contenido_excavador[i])
                lista_de_excavadores.append(contenido_excavador)
    return lista_de_excavadores


def obtener_excavadores(cantidad: int) -> list:
    """Entrega una lista que contiene
    cantidad de excavadores deseada"""
    excavadores = lista_excavadores()
    excavadores_seleccionados = sample(excavadores, k=cantidad)
    return excavadores_seleccionados


# Consumibles

def lista_consumibles() -> list:
    """Entrega una lista de listas que
    contiene a los consumibles"""
    lista_de_consumibles = []
    with open(CSV_CONSUMIBLES, "rt", encoding="utf-8") as f:
        for linea in f:
            contenido = linea.strip()
            if not contenido.endswith("felicidad"):
                contenido_consumible = contenido.split(",")
                for i in range(2, 6):
                    contenido_consumible[i] = int(contenido_consumible[i])
                lista_de_consumibles.append(contenido_consumible)
    return lista_de_consumibles


# Tesoros

def lista_tesoros() -> list:
    """Entrega una lista de listas que
    contiene a los tesoros"""
    lista_de_tesoros = []
    with open(CSV_TESOROS, "rt", encoding="utf-8") as f:
        for linea in f:
            contenido = linea.strip()
            if not contenido.endswith("cambio"):
                contenido_tesoro = contenido.split(",")
                contenido_tesoro[2] = int(contenido_tesoro[2])
                lista_de_tesoros.append(contenido_tesoro)
    return lista_de_tesoros


def obtener_consumible(cantidad=1) -> list:
    """Entrega un consumible.
    Si se especifica cantidad n,
    devuelve n consumibles."""
    consumibles = lista_consumibles()
    seleccionado = choices(consumibles, k=cantidad)
    if cantidad == 1:
        return seleccionado[0]
    else:
        return seleccionado


def obtener_tesoro(cantidad=1) -> list:
    """Entrega un tesoro.
    Si se especifica cantidad n,
    devuelve n tesoros"""
    tesoros = lista_tesoros()
    seleccionado = choices(tesoros, k=cantidad)
    if cantidad == 1:
        return seleccionado[0]
    else:
        return seleccionado
