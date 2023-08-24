from parametros import CANTIDAD_VIDAS
from PyQt5.QtCore import QObject


class Luigi(QObject):
    def __init__(self, posicion: tuple, id: int) -> None:
        self.vidas = CANTIDAD_VIDAS
        self.posicion = posicion
        self.nombre = "luigi"
        self.id = id

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion
