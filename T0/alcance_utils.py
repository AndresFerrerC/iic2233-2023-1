def alcance_x(tablero: list, abscisa: int, ordenada: int) -> int:
    """Devuelve la cantidad de celdas X que se
    recorren antes de alcanzar una tortuga a partir de
    un punto que no es contado"""
    alcance = 0
    for i in range(1, len(tablero)):
        if abscisa - i >= 0:
            if tablero[abscisa - i][ordenada] == "T":
                break
            alcance += 1
    for j in range(1, len(tablero)):
        if abscisa + j < len(tablero):
            if tablero[abscisa + j][ordenada] == "T":
                break
            alcance += 1
    return alcance


def alcance_y(tablero: list, abscisa: int, ordenada: int) -> int:
    """Devuelve la cantidad de celdas Y que se
    recorren antes de alcanzar una tortuga a partir de
    un punto que no es contado"""
    alcance = 0
    for i in range(1, len(tablero)):
        if ordenada - i >= 0:
            if tablero[abscisa][ordenada - i] == "T":
                break
            alcance += 1
    for j in range(1, len(tablero)):
        if ordenada + j < len(tablero):
            if tablero[abscisa][ordenada + j] == "T":
                break
            alcance += 1
    return alcance


def alcance_x_lista(tablero: list, abscisa: int, ordenada: int) -> list:
    """Devuelve la lista de celdas X que se
    recorren antes de alcanzar una tortuga a partir de
    un punto que no es contado"""
    alcance_x = []
    for i in range(1, len(tablero)):
        if abscisa - i >= 0:
            if tablero[abscisa - i][ordenada] == "T":
                break
            alcance_x.append((abscisa - i, ordenada))
    for j in range(1, len(tablero)):
        if abscisa + j < len(tablero):
            if tablero[abscisa + j][ordenada] == "T":
                break
            alcance_x.append((abscisa + j, ordenada))
    return alcance_x


def alcance_y_lista(tablero: list, abscisa: int, ordenada: int) -> int:
    """Devuelve la lista de celdas Y que se
    recorren antes de alcanzar una tortuga a partir de
    un punto que no es contado"""
    alcance_y = []
    for i in range(1, len(tablero)):
        if ordenada - i >= 0:
            if tablero[abscisa][ordenada - i] == "T":
                break
            alcance_y.append((abscisa, ordenada - i))
    for j in range(1, len(tablero)):
        if ordenada + j < len(tablero):
            if tablero[abscisa][ordenada + j] == "T":
                break
            alcance_y.append((abscisa, ordenada + j))
    return alcance_y


def alcance_x_bomba(tablero: list, abscisa: int, ordenada: int) -> list:
    """Devuelve la lista de celdas X que se
    recorren antes de alcanzar OTRA BOMBA"""
    alcance_x = []
    for i in range(1, len(tablero)):
        if abscisa - i >= 0:
            if tablero[abscisa - i][ordenada] != "-":
                break
            alcance_x.append((abscisa - i, ordenada))
    for j in range(1, len(tablero)):
        if abscisa + j < len(tablero):
            if tablero[abscisa + j][ordenada] != "-":
                break
            alcance_x.append((abscisa + j, ordenada))
    return alcance_x


def alcance_y_bomba(tablero: list, abscisa: int, ordenada: int) -> int:
    """Devuelve la lista de celdas Y que se
    recorren antes de alcanzar OTRA BOMBA"""
    alcance_y = []
    for i in range(1, len(tablero)):
        if ordenada - i >= 0:
            if tablero[abscisa][ordenada - i] != "-":
                break
            alcance_y.append((abscisa, ordenada - i))
    for j in range(1, len(tablero)):
        if ordenada + j < len(tablero):
            if tablero[abscisa][ordenada + j] != "-":
                break
            alcance_y.append((abscisa, ordenada + j))
    return alcance_y


def alcance_tortuga_unica(tablero: list, abscisa: int, ordenada: int) -> int:
    """Devuelve cantidad de tortugas que estén rodeando a la de coordenada."""
    topan = 0
    if abscisa + 1 < len(tablero):
        if tablero[abscisa + 1][ordenada] == "T":
            topan += 1
    if abscisa - 1 >= 0:
        if tablero[abscisa - 1][ordenada] == "T":
            topan += 1
    if ordenada + 1 < len(tablero):
        if tablero[abscisa][ordenada + 1] == "T":
            topan += 1
    if ordenada - 1 >= 0:
        if tablero[abscisa][ordenada - 1] == "T":
            topan += 1
    return topan
