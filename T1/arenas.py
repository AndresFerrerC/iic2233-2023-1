from abc import ABC
import flujo_torneo as flujo


class Arena(ABC):
    def __init__(self, nombre: str, rareza: int, humedad: int,
                 dureza: int, estatica: int, tipo=None) -> None:
        self.nombre = nombre
        self.tipo = tipo
        self.items = flujo.obtener_items_instanciados()
        self.__rareza = rareza
        self.__humedad = humedad
        self.__dureza = dureza
        self.__estatica = estatica
        self.__dificultad = round((self.__rareza + self.__humedad +
                                   self.__dureza + self.__estatica) / 40, 2)

    @property
    def rareza(self):
        return self.__rareza

    @rareza.setter
    def rareza(self, nueva):
        if nueva >= 10:
            self.__rareza = 10
        elif nueva <= 1:
            self.__rareza = 1
        else:
            self.__rareza = nueva

    @property
    def humedad(self):
        return self.__humedad

    @humedad.setter
    def humedad(self, nueva):
        if nueva >= 10:
            self.__humedad = 10
        elif nueva <= 1:
            self.__humedad = 1
        else:
            self.__humedad = nueva

    @property
    def dureza(self):
        return self.__dureza

    @dureza.setter
    def dureza(self, nueva):
        if nueva >= 10:
            self.__dureza = 10
        elif nueva <= 1:
            self.__dureza = 1
        else:
            self.__dureza = nueva

    @property
    def estatica(self):
        return self.__estatica

    @estatica.setter
    def estatica(self, nueva):
        if nueva >= 10:
            self.__estatica = 10
        elif nueva <= 1:
            self.__estatica = 1
        else:
            self.__estatica = nueva

    @property
    def dificultad(self):
        return self.__dificultad

    @dificultad.setter
    def dificultad(self, nueva):
        if nueva >= 1:
            self.__dificultad = 1
        elif nueva <= 0:
            self.__dificultad = 0
        else:
            posible = round(nueva, 2)
            if posible == 0.00:
                self.__dificultad = 0.01  # Prevenir ZeroDivision
            else:
                self.__dificultad = round(nueva, 2)


class ArenaNormal(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "normal"


class ArenaMojada(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "mojada"


class ArenaRocosa(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "rocosa"
        self.suma = self.rareza + self.humedad + self.estatica + \
            (2 * self.dureza)
        self.ponderador = self.suma / 50
        self.dificultad = self.ponderador  # setter redondea a 2


class ArenaMagnetica(ArenaMojada, ArenaRocosa):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "magnetica"
