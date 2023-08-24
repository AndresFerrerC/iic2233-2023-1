# Agregar los imports que estimen necesarios
import copy
import alcance_utils as alcance

def cargar_tablero(nombre_archivo: str) -> list:
    """Devuelve una lista de listas correspondiente al tablero
    del juego, a partir de un path que es el nombre de archivo."""
    tablero = []
    with open(nombre_archivo, "rt") as archivo:
        primera_linea = archivo.readline().strip("\n")
        lista_linea = primera_linea.split(",")
        n = int(lista_linea.pop(0))  # tamaño tablero y elimina de lista
        recorrido = 0  # indice de lista linea actualizada
        tablero = [[] for n in range(n)]  # [ [] , ... n veces ].
        for i in range(n):
            for j in range(n):
                valor_lista_actual = lista_linea[recorrido]
                tablero[i].append(valor_lista_actual)
                recorrido += 1
    return tablero


def guardar_tablero(nombre_archivo: str, tablero: list) -> None:
    """Recibe un path con el nombre del archivo y un tablero.
    Guarda en el formato n,objeto,objeto ...."""
    guardar = [str(len(tablero))]
    for subtablero in tablero:
        guardar += subtablero
    with open(nombre_archivo, "wt") as archivo:
        print((",").join(guardar), end='', file=archivo)


def verificar_valor_bombas(tablero: list) -> int:
    """Verifica que las bombas cumplan con tener un valor
    mínimo de 2 y uno máximo de 2n-1. Devuelve cantidad de
    bombas que no cumplen con esta norma"""
    bombas_invalidas = 0
    minimo_valor = 2
    maximo_valor = 2 * len(tablero) - 1
    for sub_lista in tablero:
        for posicion in sub_lista:  # "-", "T", etc.
            if posicion != "-" and posicion != "T":  # bomba
                valor_bomba = int(posicion)
                if valor_bomba < minimo_valor or valor_bomba > maximo_valor:
                    bombas_invalidas += 1
    return bombas_invalidas


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    """Devuelve el alcance de cada bomba, incluyendo a sí misma,
    antes de topar con tortugas. Si no es bomba, devuelve 0."""
    coord_x = coordenada[0]  # fila
    coord_y = coordenada[1]  # columna
    objeto = tablero[coord_x][coord_y]
    if objeto != "T" and objeto != "-":
        return alcance.alcance_x(tablero, coord_x,  coord_y) + \
           alcance.alcance_y(tablero, coord_x, coord_y) + 1  # ella misma tb
    return 0


def verificar_bombas(tablero: list) -> bool:
    """Comprueba regla 1. Verifica que toda bomba cumpla
    con tener un número igual a su alcance. True en caso de cumplir."""
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] != "T" and tablero[i][j] != "-":
                valor_bomba = int(tablero[i][j])
                valor_verificado = verificar_alcance_bomba(tablero, (i, j))
                if valor_verificado != valor_bomba:
                    return False
    return True


def alcance_bombas_invalidas(tablero: list) -> int:
    """Entrega alcance total de bombas invalidas."""
    total = 0
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] != "T" and tablero[i][j] != "-":
                valor_bomba = int(tablero[i][j])
                valor_verificado = verificar_alcance_bomba(tablero, (i, j))
                if valor_verificado > valor_bomba:
                    total += valor_verificado
    return total


def verificar_regla_tres(tablero: list) -> bool:
    """Comprueba regla 3. NO pueden haber celdas con tortugas
    y bombas a la vez. Devuelve True si es que se cumple."""
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if len(str(tablero[i][j])) > 1:
                if "T" in tablero[i][j]:
                    return False
    return True


def alcance_tortugas(tablero: list, coordenadas: tuple) -> list:
    """Devuelve lista de tuplas conteniendo las coordenadas
    de las tortugas que topan con la de la coordenada (x, y)
    Es decir, aquellas tortugas que estén inmediatamente
    abajo o al lado de la tortuga dada."""
    abscisa = coordenadas[0]
    ordenada = coordenadas[1]
    posiciones = []
    if abscisa + 1 < len(tablero):
        if tablero[abscisa + 1][ordenada] == "T":
            posiciones.append((abscisa + 1, ordenada))
    if ordenada + 1 < len(tablero):
        if tablero[abscisa][ordenada + 1] == "T":
            posiciones.append((abscisa, ordenada + 1))
    return posiciones


def verificar_tortugas(tablero: list) -> int:
    """Devuelve cantidad de tortugas contiguas"""
    recorrido = []
    largo = len(tablero)
    for i in range(largo):
        for j in range(largo):
            objeto = tablero[i][j]
            if objeto == "T":
                posiciones = alcance_tortugas(tablero, (i, j))
                if len(posiciones) > 0:  # tortuga abajo/lado
                    if (i, j) not in recorrido:
                        recorrido.append((i, j))
                    [recorrido.append(posicion) for posicion in posiciones
                     if posicion not in recorrido]
    tortugas_incumplen = len(recorrido)
    return tortugas_incumplen


def verificar_isla_vertical(tablero: list, coordenadas: tuple) -> bool:
    """Retorna True si la coordenada (x,y) NO tiene islas verticales"""
    coordenada_x = coordenadas[0]
    coordenada_y = coordenadas[1]
    largo_lista = len(tablero)
    no_islas = False
    if coordenada_x + 1 < largo_lista:
        if tablero[coordenada_x + 1][coordenada_y] != "T":
            no_islas = True
    if coordenada_x - 1 >= 0:
        if tablero[coordenada_x - 1][coordenada_y] != "T":
            no_islas = True
    return no_islas


def verificar_isla_horizontal(tablero: list, coordenadas: tuple) -> bool:
    """Retorna True si la coordenada (x,y) NO tiene islas horizontales"""
    coordenada_x = coordenadas[0]
    coordenada_y = coordenadas[1]
    largo_lista = len(tablero)
    no_islas = False
    if coordenada_y + 1 < largo_lista:
        if tablero[coordenada_x][coordenada_y + 1] != "T":
            no_islas = True
    if coordenada_y - 1 >= 0:
        if tablero[coordenada_x][coordenada_y - 1] != "T":
            no_islas = True
    return no_islas


def verificar_islas(tablero: list) -> bool:
    """Retorna True si es que existen celdas aisladas"""
    largo = len(tablero)
    topa = False
    for i in range(largo):
        for j in range(largo):
            if tablero[i][j] != "T":
                islas_verticales = verificar_isla_vertical(tablero, (i, j))
                islas_horizontales = verificar_isla_horizontal(tablero, (i, j))
                if not islas_verticales and not islas_horizontales:
                    # hay algo aislado vertical y horizontalmente
                    topa = True
                    break
    return topa


def cumple_reglas(tablero: list) -> bool:
    """Devuelve True si el tablero cumple con las reglas 1 a 5"""
    cumple_regla_1 = verificar_bombas(tablero)
    cumple_regla_2 = verificar_valor_bombas(tablero) == 0
    cumple_regla_3 = verificar_regla_tres(tablero)
    cumple_regla_4 = verificar_tortugas(tablero) == 0
    cumple_regla_5 = verificar_islas(tablero) is False
    return cumple_regla_1 and cumple_regla_2 and \
        cumple_regla_3 and cumple_regla_4 and cumple_regla_5


def celdas_intocables(tablero: list) -> list:
    """Devuelve la lista con celdas intocables
    en caso de que se tenga una bomba exacta,
    donde si se agregan tortugas cerca, se corrompe"""
    intocables = []
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] != "T" and tablero[i][j] != "-":  # bomba
                bomba = int(tablero[i][j])
                if verificar_alcance_bomba(tablero, (i, j)) == bomba:
                    # cumple con su alcance
                    intocables += alcance.alcance_x_lista(tablero, i, j)
                    intocables += alcance.alcance_y_lista(tablero, i, j)
    return intocables


def muerte_por_alcance(tablero: list, abscisa: int, ordenada: int) -> bool:
    """Devuelve True si es que es imposible agregar tortugas
    para la bomba en (x,y), tal que se arregle su alcance
    (se disminuya)."""
    alcance_h = alcance.alcance_y(tablero, abscisa, ordenada)
    alcance_v = alcance.alcance_x(tablero, abscisa, ordenada)
    alcance_lista_bomba_h = alcance.alcance_y_bomba(tablero, abscisa, ordenada)
    alcance_lista_bomba_v = alcance.alcance_x_bomba(tablero, abscisa, ordenada)
    bomba = int(tablero[abscisa][ordenada])
    if alcance_v == 0 and alcance_h == 0:
        return True
    if alcance_h == 0 and alcance_v + 1 > bomba:
        if len(alcance_lista_bomba_v) < bomba:
            return True
    if alcance_v == 0 and alcance_h + 1 > bomba:
        if len(alcance_lista_bomba_h) < bomba:
            return True
    return False


def tablero_muerto(tablero: list) -> bool:
    """Devuelve True si es que existen bombas
    con un alcance menor a su número dentro del tablero"""
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] != "T" and tablero[i][j] != "-":  # bomba
                bomba = int(tablero[i][j])
                if verificar_alcance_bomba(tablero, (i, j)) < bomba:
                    return True
                if muerte_por_alcance(tablero, i, j):
                    return True
    return False


def posibles_tortugas(tablero: list, posicion: tuple) -> list:
    """Devuelve una lista con posibles ubicaciones para
    poner tortugas dada la bomba en posición (x, y)"""
    x, y = posicion
    posibles = []
    previa = alcance.alcance_y_lista(tablero, x, y) + \
        alcance.alcance_x_lista(tablero, x, y)
    [posibles.append(posicion) for posicion in previa if
     tablero[posicion[0]][posicion[1]] == "-"]
    return posibles


def lista_posibles_tortugas(tablero: list, camino: list):
    """Devuelve una lista con todas las posibles tortugas a 
    poner dentro del tablero"""
    lista_preliminar = []
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] != "-" and tablero[i][j] != "T":
                alcance = int(tablero[i][j])
                if verificar_alcance_bomba(tablero, (i, j)) != alcance:
                    lista_preliminar += posibles_tortugas(tablero, (i, j))
    lista_bombas = []
    intocables = celdas_intocables(tablero)
    [lista_bombas.append(posicion) for posicion in lista_preliminar
     if posicion not in lista_bombas and posicion not in camino and
     posicion not in intocables]
    return lista_bombas


def es_valida(tablero: list, posicion: tuple, ruta_actual: list) -> bool:
    """Devuelve True si la posición es MÍNIMAMENTE
    válida para poner una tortuga"""
    x, y = posicion
    if not (0 <= x < len(tablero) and 0 <= y < len(tablero)):
        return False
    if tablero[x][y] != "-":
        return False
    if alcance.alcance_tortuga_unica(tablero, x, y) != 0:
        return False
    if posicion in ruta_actual:
        return False
    return True


def obtener_tabla(tablero: list, camino: list) -> list:
    """Devuelve un tablero solucionado"""
    if cumple_reglas(tablero):
        return tablero
    posibles = lista_posibles_tortugas(tablero, camino)
    for posible in posibles:
        if es_valida(tablero, posible, camino):
            alcance = alcance_bombas_invalidas(tablero)
            tablero[posible[0]][posible[1]] = "T"
            nuevo_alcance = alcance_bombas_invalidas(tablero)
            if nuevo_alcance < alcance and not tablero_muerto(tablero):
                solucion = obtener_tabla(tablero, camino + [posible])
                if solucion != []:
                    return solucion
            tablero[posible[0]][posible[1]] = "-"
    return []


def solucionar_tablero(tablero: list) -> list:
    tablero_alterable = copy.deepcopy(tablero)
    tablero_solucionado = obtener_tabla(tablero_alterable, [])
    if tablero_solucionado != []:
        return tablero_solucionado
    return None


if __name__ == "__main__":
    tablero_2x2 = [
        ['-', 2],
        ['-', '-']
    ]
    resultado = verificar_valor_bombas(tablero_2x2)
    print(resultado)  # Debería ser 0

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 3

    tablero_resuelto = solucionar_tablero(tablero_2x2)
    print(tablero_resuelto)

    tablero_2x2_sol = [
        ['T', 2],
        ['-', '-']
    ]

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 2

    resultado = verificar_tortugas(tablero_2x2_sol)
    print(resultado)  # Debería ser 0
