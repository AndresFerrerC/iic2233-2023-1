from PyQt5.QtCore import QObject


class Estrella(QObject):
    def __init__(self, posicion: tuple, id: int) -> None:
        self.posicion = posicion
        self.nombre = "estrella"
        self.id = id

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion


class Pared(QObject):
    def __init__(self, posicion: tuple, id: int) -> None:
        self.posicion = posicion
        self.nombre = "pared"
        self.id = id

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion


class Roca(QObject):
    def __init__(self, posicion: tuple, id: int) -> None:
        self.posicion = posicion
        self.nombre = "roca"
        self.id = id

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion


class Fuego(QObject):
    def __init__(self, posicion: tuple, id: int) -> None:
        self.posicion = posicion
        self.id = id
        self.nombre = "fuego"

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion
