from abc import ABC


class Item(ABC):
    def __init__(self, nombre, descripcion, tipo) -> None:
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion


class Consumibles(Item):
    def __init__(self, nombre, descripcion, energia, fuerza, suerte,
                 felicidad) -> None:
        super().__init__(nombre, descripcion, tipo="consumible")
        self.energia = energia
        self.fuerza = fuerza
        self.suerte = suerte
        self.felicidad = felicidad


class Tesoros(Item):
    def __init__(self, nombre, descripcion, calidad, cambio) -> None:
        super().__init__(nombre, descripcion, tipo="tesoro")
        self.calidad = calidad
        self.cambio = cambio
