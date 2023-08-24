from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from parametros import ICONOS_BLOQUES, ICONOS_ENTIDADES, PATH_SPRITES, \
    PATH_BORDER, LISTA_BLOQUES, LISTA_ENTIDADES, PATH_MAPAS, LARGO_GRILLA, \
    ANCHO_GRILLA
import os
import backend.luigi as backend_luigi
import backend.fantasmas as backend_fantasmas
import backend.objetos as backend_objetos


def obtener_mapas() -> dict:
    """Devuelve los mapas disponibles y su ID"""
    id = 1  # Para el selector
    carpeta = os.path.join(*PATH_MAPAS)
    posibles_opciones = os.listdir(carpeta)
    mapas = {}
    for i in range(len(posibles_opciones)):
        archivo = os.path.splitext(posibles_opciones[i])
        if archivo[1] == ".txt":
            mapas[id] = archivo[0]
            id += 1
    return mapas


def obtener_posiciones_bordes() -> set:
    """Retorna un set con las
    posiciones [i][j] de los bordes"""
    return set([(i, 0) for i in range(LARGO_GRILLA)]
               + [(0, j) for j in range(ANCHO_GRILLA)]
               + [(i, 10) for i in range(LARGO_GRILLA)]
               + [(15, j) for j in range(ANCHO_GRILLA)])


def obtener_casilla(casillas: list, posicion: tuple) -> list:
    """Retorna posición (i, j) de la casilla dadas las coordenadas
    Formato [Bool, (i, j)]. True si (x,y) pertenece a la grilla."""
    x, y = posicion[0], posicion[1]
    for i in range(LARGO_GRILLA):
        for j in range(ANCHO_GRILLA):
            casilla = casillas[i][j]
            casilla_x = casilla.x()
            casilla_y = casilla.y()
            if (i, j) not in obtener_posiciones_bordes():
                if x >= casilla_x and x < casilla_x + 32:
                    if y >= casilla_y and y < casilla_y + 32:
                        return [True, (i, j)]
    return [False, (0, 0)]


def obtener_ubicacion_casilla(casillas: list, posicion: tuple) -> tuple:
    """Retorna la ubicación absoluta (x, y) dada una casilla [i][j]"""
    i, j = posicion[0], posicion[1]
    return (casillas[i][j].x(), casillas[i][j].y())


def obtener_nueva_posicion(tipo_movimiento: str,
                           posicion_actual: tuple) -> tuple:
    """Retorna una tupla con la nueva posición en la grilla
    dada el tipo de movimiento que se especifique"""
    posicion_x = posicion_actual[0]
    posicion_y = posicion_actual[1]
    if tipo_movimiento == "w":
        return (posicion_x - 1, posicion_y)
    elif tipo_movimiento == "a":
        return (posicion_x, posicion_y - 1)
    elif tipo_movimiento == "s":
        return (posicion_x + 1, posicion_y)
    elif tipo_movimiento == "d":
        return (posicion_x, posicion_y + 1)


def estilizar_casilla(label: object) -> None:
    """Estiliza una casilla con el color de fondo y borde"""
    label.setStyleSheet(
        """
        background-color: #2D2C2C; border: 0.5px solid #1f1f1f;
    """
    )


def instalar_iconos() -> dict:
    """Retorna dict con los QIcon de
    los elementos para usar en los botones"""
    iconos = {}
    for elemento in ICONOS_BLOQUES:
        ruta = os.path.join(*PATH_SPRITES, "Elementos",
                            ICONOS_BLOQUES[elemento])
        iconos[elemento] = QIcon(ruta)
    for personaje in ICONOS_ENTIDADES:
        ruta = os.path.join(*PATH_SPRITES, "Personajes",
                            ICONOS_ENTIDADES[personaje])
        iconos[personaje] = QIcon(ruta)
    return iconos


def instalar_iconos_casillas() -> dict:
    """Retorna dict con los QPixmap
    de los elementos para usar en las casillas"""
    ruta_borde = os.path.join(*PATH_BORDER)
    imagenes = {}
    for elemento in ICONOS_BLOQUES:
        ruta = os.path.join(*PATH_SPRITES, "Elementos",
                            ICONOS_BLOQUES[elemento])
        imagenes[elemento] = QPixmap(ruta)
    for personaje in ICONOS_ENTIDADES:
        ruta = os.path.join(*PATH_SPRITES, "Personajes",
                            ICONOS_ENTIDADES[personaje])
        imagenes[personaje] = QPixmap(ruta)
    imagenes["borde"] = QPixmap(ruta_borde)
    return imagenes


def crear_diccionario_posiciones() -> dict:
    """Crea un diccionario con listas vacías
    para almacenar posiciones o entidades instanciadas"""
    posicion_elementos = dict()
    for nombre in LISTA_BLOQUES + LISTA_ENTIDADES:
        posicion_elementos[nombre] = []
    return posicion_elementos


def limpiar_layout(layout: object) -> None:
    """Limpia los elementos del layout"""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def alertar(texto: str, tipo: str) -> None:
    """Retorna una alerta con contenido 'texto'
    del tipo 'tipo'; Warning, Information, etc."""
    box_alerta = QMessageBox()
    if tipo == "warning":
        box_alerta.setIcon(QMessageBox.Warning)
    else:
        box_alerta.setIcon(QMessageBox.Information)  # Por defecto
    box_alerta.setText(texto)
    box_alerta.setWindowTitle("Alerta")  # <- Se ignora en MacOS
    box_alerta.exec()


def instanciar_personaje_backend(personaje: str, posicion: tuple,
                                 id: int) -> object:
    """Devuelve un personaje del backend instanciado"""
    if personaje == "luigi":
        return backend_luigi.Luigi(posicion, id)
    elif personaje == "fantasma_vertical":
        return backend_fantasmas.FantasmaVertical(posicion, id)
    elif personaje == "fantasma_horizontal":
        return backend_fantasmas.FantasmaHorizontal(posicion, id)
    elif personaje == "fantasma_followervillain":
        return backend_fantasmas.FantasmaFollowerVillain(posicion, id)
    elif personaje == "pared":
        return backend_objetos.Pared(posicion, id)
    elif personaje == "roca":
        return backend_objetos.Roca(posicion, id)
    elif personaje == "fuego":
        return backend_objetos.Fuego(posicion, id)
    elif personaje == "estrella":
        return backend_objetos.Estrella(posicion, id)


def posicion_valida(posicion: tuple) -> bool:
    """Retorna True si la posición es válida"""
    posicion_i, posicion_j = posicion[0], posicion[1]
    if posicion_i < 0 or posicion_i > LARGO_GRILLA - 2:
        return False
    if posicion_j < 0 or posicion_j > ANCHO_GRILLA - 2:
        return False
    return True


def casilla_alcanzable(posicion_inicio: tuple, tipo_movimiento: str,
                       posicion_final: str, posiciones_bloqueadas: set) -> bool:
    """Retorna True si es que la casilla se puede alcanzar
    siguiendo únicamente movimientos en la dirección dada"""
    x_final, y_final = posicion_final[0], posicion_final[1]
    x_inicio, y_inicio = posicion_inicio[0], posicion_inicio[1]
    while (x_final != x_inicio or y_final != y_inicio) and posicion_valida(
                                                    (x_inicio, y_inicio)):
        if tipo_movimiento == "w":
            x_inicio -= 1
        elif tipo_movimiento == "s":
            x_inicio += 1
        elif tipo_movimiento == "a":
            y_inicio -= 1
        elif tipo_movimiento == "d":
            y_inicio += 1
        if (x_inicio, y_inicio) in posiciones_bloqueadas:
            if (x_inicio, y_inicio) not in obtener_posiciones_bordes():
                return False
    return True


def obtener_distancia_casillas(posicion_inicio: tuple,
                               posicion_fin: tuple) -> int:
    """Retorna la distancia entre las casillas"""
    distancia_x = abs(posicion_inicio[0] - posicion_fin[0])
    distancia_y = abs(posicion_inicio[1] - posicion_fin[1])
    return distancia_x + distancia_y
