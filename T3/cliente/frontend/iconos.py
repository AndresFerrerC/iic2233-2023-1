from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import auxiliares as auxiliar
import os


class Usuario(QLabel):
    path_parametros = "parametros.json"
    parametros = auxiliar.leer_archivo_json(path_parametros)

    def __init__(self, parent: object, posicion: tuple,
                 ponderador_tamano=1) -> None:
        """Inicializa la clase heredada de QLabel"""
        super().__init__(parent)
        self.posicion_inicial = posicion
        self.ponderador = ponderador_tamano
        self.instalar_personaje()
        self.setScaledContents(True)

    def instalar_personaje(self) -> None:
        """Instala el ícono en las coordenadas iniciales (x, y)"""
        ubicacion_imagen = self.parametros["path_extra"] + \
            [self.parametros["imagenes_extra"]["perfil"]]
        path_imagen = os.path.join(*ubicacion_imagen)
        pixmap_imagen = QPixmap(path_imagen)
        self.pixmap_principal = pixmap_imagen
        self.setPixmap(self.pixmap_principal)
        self.dimensiones = (int(100 * self.ponderador),
                            int(100 * self.ponderador))
        self.setGeometry(*self.posicion_inicial, *self.dimensiones)


class Dado(QLabel):
    path_parametros = "parametros.json"
    parametros = auxiliar.leer_archivo_json(path_parametros)

    def __init__(self, parent: object, posicion: tuple, numero=None) -> None:
        """Inicializa la clase heredada de QLabel"""
        super().__init__(parent)
        self.posicion_inicial = posicion
        self.numero = numero
        self.instalar_elemento()
        self.setScaledContents(True)

    def instalar_elemento(self) -> None:
        """Inicializa el ícono en las coordenadas iniciales"""
        self.instanciar_imagenes()
        self.actualizar_valor(self.numero)
        self.dimensiones = (40, 40)
        self.setGeometry(*self.posicion_inicial, *self.dimensiones)

    def instanciar_imagenes(self) -> None:
        """Instancia los QPixmap de los dados"""
        self.sprites = {}
        path_dices = self.parametros["path_dices"]
        for i in range(1, 7):
            ubicacion = path_dices + [self.parametros["imagenes_dados"][f"{i}"]]
            path_imagen = os.path.join(*ubicacion)
            self.sprites[i] = QPixmap(path_imagen)
        ubicacion_logo = path_dices + [self.parametros["imagenes_dados"]["logo"]]
        ubicacion_fondo = path_dices + [self.parametros["imagenes_dados"]["fondo"]]
        self.sprites["logo"] = QPixmap(os.path.join(*ubicacion_logo))
        self.sprites["fondo"] = QPixmap(os.path.join(*ubicacion_fondo))

    def actualizar_valor(self, numero_str: str) -> None:
        """Actualiza el dado. Acepta números del 1 al 6, además
         de -1 y otro, donde -1 es logo y otro es background."""
        if not str(numero_str).isnumeric():
            numero = -2
        else:
            numero = int(numero_str)
        if numero >= 1 and numero <= 6:
            self.setPixmap(self.sprites[numero])
        elif numero == -1:
            self.setPixmap(self.sprites["logo"])
        else:
            self.setPixmap(self.sprites["fondo"])
        self.numero = numero
