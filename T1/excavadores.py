from __future__ import annotations
from items import Consumibles
from abc import ABC
from random import random, choices
from parametros import FELICIDAD_ADICIONAL_DOCENCIO, EDAD_ADICIONAL_TAREO, \
    ENERGIA_PERDIDA_DOCENCIO, ENERGIA_ADICIONAL_TAREO, \
    FUERZA_ADICIONAL_DOCENCIO, SUERTE_ADICIONAL_TAREO, PROB_ENCONTRAR_ITEM, \
    PROB_ENCONTRAR_TESORO, PROB_ENCONTRAR_CONSUMIBLE, FELICIDAD_PERDIDA_TAREO


class Excavador(ABC):
    def __init__(self, nombre: str, edad: int, energia: int, fuerza: int,
                 suerte: int, felicidad: int, tipo=None,
                 descansando=[False, 0, 0]) -> None:
        self.tipo = tipo
        self.nombre = nombre
        self.descansando = descansando  # estado, días, transcurridos
        self.__edad = 0
        self.__energia = 0
        self.__fuerza = 0
        self.__suerte = 0
        self.__felicidad = 0
        # Llama a setters que se aseguran de datos adecuados en args.
        self.edad = edad
        self.energia = energia
        self.fuerza = fuerza
        self.suerte = suerte
        self.felicidad = felicidad

    @property
    def edad(self) -> int:
        return self.__edad

    @edad.setter
    def edad(self, nueva) -> None:
        if nueva <= 18:
            self.__edad = 18
        elif nueva >= 60:
            self.__edad = 60
        else:
            self.__edad = nueva

    @property
    def energia(self) -> int:
        return self.__energia

    @energia.setter
    def energia(self, nueva) -> None:
        if nueva <= 0:
            self.__energia = 0
        elif nueva >= 100:
            self.__energia = 100
        else:
            self.__energia = nueva

    @property
    def fuerza(self) -> int:
        return self.__fuerza

    @fuerza.setter
    def fuerza(self, nueva) -> None:
        if nueva <= 1:
            self.__fuerza = 1
        elif nueva >= 10:
            self.__fuerza = 10
        else:
            self.__fuerza = nueva

    @property
    def suerte(self) -> int:
        return self.__suerte

    @suerte.setter
    def suerte(self, nueva) -> None:
        if nueva <= 1:
            self.__suerte = 1
        elif nueva >= 10:
            self.__suerte = 10
        else:
            self.__suerte = nueva

    @property
    def felicidad(self) -> int:
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, nueva) -> None:
        if nueva <= 1:
            self.__felicidad = 1
        elif nueva >= 10:
            self.__felicidad = 10
        else:
            self.__felicidad = nueva

    def cavar(self, dificultad: float) -> float:
        """Retorna un float con los metros cavados."""
        primer_termino = 30 / self.edad
        segundo_termino = (self.felicidad + (2 * self.fuerza)) / 10
        suma = primer_termino + segundo_termino
        multiplo = (1 / (10 * dificultad))
        cavados = round(suma * multiplo, 2)
        print(f"{self.nombre} ha cavado {cavados} metros.")
        return cavados

    def descansar(self) -> None:
        """Establece el estado de descanso
        y hace print de aquello."""
        dias_descanso = int(self.edad / 20)
        self.descansando = [True, dias_descanso, 0]
        print(f"{self.nombre} decidió descansar por {dias_descanso} días...")

    def encontrar_item(self, tipo_arena: str) -> str:
        """Retorna el tipo de item a encontrar.
        Si la arena es mojada o magnética, 100% de encontrar."""
        evento_final = None
        if tipo_arena == "mojada" or tipo_arena == "magnetica":
            probabilidad = 1
        else:
            probabilidad = PROB_ENCONTRAR_ITEM * (self.suerte / 10)

        if random() <= probabilidad:
            posibles = ["consumible", "tesoro"]
            if tipo_arena == "mojada":
                pesos = [0.5, 0.5]
            else:
                pesos = [PROB_ENCONTRAR_CONSUMIBLE, PROB_ENCONTRAR_TESORO]
            evento_iniciado = choices(posibles, weights=pesos, k=1)
            evento_final = evento_iniciado[0]
        return evento_final

    def gastar_energia(self) -> None:
        """Gasta energía."""
        energia_gastada = int((10 / self.fuerza) + (self.edad / 6))
        self.energia -= energia_gastada

    def consumir(self, consumible: Consumibles) -> None:
        """Consume un elemento del tipo consumible"""
        self.energia += consumible.energia
        self.fuerza += consumible.fuerza
        self.suerte += consumible.suerte
        self.felicidad += consumible.felicidad


class ExcavadorDocencio(Excavador):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "docencio"

    def cavar(self, dificultad: float) -> float:  # overriding
        """Retorna un float con los metros cavados.
        Overriding se produce por variaciones en el tipo
        de excavador."""
        primer_termino = 30 / self.edad
        segundo_termino = (self.felicidad + (2 * self.fuerza)) / 10
        suma = primer_termino + segundo_termino
        multiplo = (1 / (10 * dificultad))
        cavados = round(suma * multiplo, 2)
        self.felicidad += FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += FUERZA_ADICIONAL_DOCENCIO
        self.energia -= ENERGIA_PERDIDA_DOCENCIO
        print(f"{self.nombre} ha cavado {cavados} metros.")
        return cavados


class ExcavadorTareo(Excavador):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "tareo"

    def consumir(self, consumible: Consumibles) -> None:
        """Consume un elemento del tipo consumible"""
        self.energia += consumible.energia + ENERGIA_ADICIONAL_TAREO
        self.fuerza += consumible.fuerza
        self.suerte += consumible.suerte + SUERTE_ADICIONAL_TAREO
        self.felicidad += consumible.felicidad - FELICIDAD_PERDIDA_TAREO
        self.edad += EDAD_ADICIONAL_TAREO


class ExcavadorHibrido(ExcavadorDocencio, ExcavadorTareo):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "hibrido"

    # La energía no podrá descender de los 20. Override.
    @Excavador.energia.setter
    def energia(self, nueva) -> None:
        if nueva <= 20:
            # Acceso a atributo privado de clase padre
            self._Excavador__energia = 20
        elif nueva >= 100:
            self._Excavador__energia = 100
        else:
            self._Excavador__energia = nueva

    def gastar_energia(self) -> None:
        """Gasta energía (la mitad)."""
        energia_gastada = int((10 / self.fuerza) + (self.edad / 6))
        self.energia -= int(energia_gastada / 2)
