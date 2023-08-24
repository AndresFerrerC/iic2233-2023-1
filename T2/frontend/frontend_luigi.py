from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from parametros import IMAGENES_LUIGI, PATH_PERSONAJES, INTERVALO_SPRITES, \
    DIMENSION_SPRITES
import os


class Luigi(QLabel):
    def __init__(self, parent: object, posicion: tuple, id: int) -> None:
        """Inicializa la clase heredada de QLabel"""
        super().__init__(parent)
        self.posicion_inicial = posicion
        self.tipo_movimiento = None
        self.id = id
        self.instalar_personaje()
        self.instalar_lista_imagenes()
        self.instalar_timers()
        self.setScaledContents(True)

    def instalar_personaje(self) -> None:
        """Instala el personaje en las coordenadas iniciales (x, y)"""
        self.instanciar_imagenes()
        self.pixmap_principal = self.sprites_animaciones["front"][0]  # Front
        self.setPixmap(self.pixmap_principal)
        self.setGeometry(*self.posicion_inicial, *DIMENSION_SPRITES)

    def instanciar_imagenes(self) -> None:
        """Instancia un diccionario conteniendo referencias
        a los QPixmap de cada imagen del personaje"""
        self.sprites_animaciones = {}
        for tipo_movimiento in IMAGENES_LUIGI:
            lista_qpixmap = []
            for imagen in IMAGENES_LUIGI[tipo_movimiento]:
                path_imagen = os.path.join(*PATH_PERSONAJES, imagen)
                pixmap_imagen = QPixmap(path_imagen)
                lista_qpixmap.append(pixmap_imagen)
            self.sprites_animaciones[tipo_movimiento] = lista_qpixmap

    def instalar_lista_imagenes(self) -> None:
        """Crea las variables que referencian a los sprites"""
        self.lista_imagenes_arriba = self.sprites_animaciones["up"]
        self.lista_imagenes_abajo = self.sprites_animaciones["down"]
        self.lista_imagenes_derecha = self.sprites_animaciones["right"]
        self.lista_imagenes_izquierda = self.sprites_animaciones["left"]

    def instalar_timers(self) -> None:
        """"Instala los QTimers para la animación"""
        self.indice_lista_animacion = 0
        self.timer_animacion = QTimer()
        self.timer_animacion.setInterval(INTERVALO_SPRITES)
        self.timer_animacion.timeout.connect(self.animar)
        self.timer_detener_animacion = QTimer()
        self.timer_detener_animacion.setInterval(INTERVALO_SPRITES * 3)
        self.timer_detener_animacion.timeout.connect(self.detener_animacion)

    def animar(self) -> None:
        """Genera la animación en el personaje"""
        if self.tipo_movimiento == "front":
            self.setPixmap(self.pixmap_principal)
        else:
            if self.tipo_movimiento == "up":
                lista = self.lista_imagenes_arriba
            elif self.tipo_movimiento == "down":
                lista = self.lista_imagenes_abajo
            elif self.tipo_movimiento == "right":
                lista = self.lista_imagenes_derecha
            elif self.tipo_movimiento == "left":
                lista = self.lista_imagenes_izquierda
            indice = self.indice_lista_animacion % 3
            self.setPixmap(lista[indice])
            self.indice_lista_animacion += 1

    def detectar_tipo_movimiento(self, posicion_mapa: tuple) -> str:
        """Retorna el tipo de movimiento (up, down, left, right)
        dependiendo de las nuevas posiciones dentro del mapa"""
        posicion_x, posicion_y = self.x(), self.y()
        nueva_x, nueva_y = posicion_mapa[0], posicion_mapa[1]
        if nueva_y > posicion_y:
            return "down"
        elif nueva_y < posicion_y:
            return "up"
        elif nueva_x > posicion_x:
            return "right"
        elif nueva_x < posicion_x:
            return "left"
        else:
            return "front"  # no hay movimiento

    def comenzar_animacion(self) -> None:
        """Inicializa el timer de la animación"""
        self.timer_animacion.start()
        self.timer_detener_animacion.start()

    def detener_animacion(self) -> None:
        """Detiene la animación del personaje"""
        self.timer_animacion.stop()
        self.timer_detener_animacion.stop()
        self.setPixmap(self.pixmap_principal)
        self.indice_lista_animacion = 0

    def movimiento(self, posicion_mapa: tuple) -> None:
        """Mueve el personaje hacia la posición del mapa"""
        self.tipo_movimiento = self.detectar_tipo_movimiento(posicion_mapa)
        if self.tipo_movimiento == "front":
            self.setPixmap(self.pixmap_principal)
        else:
            self.comenzar_animacion()
            self.movimiento_casilla = QPropertyAnimation(self, b"pos")
            self.movimiento_casilla.setEndValue(QPoint(*posicion_mapa))
            self.movimiento_casilla.setDuration(INTERVALO_SPRITES * 3)
            self.movimiento_casilla.start()
