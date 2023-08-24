import auxiliares as auxiliar
from parametros import MIN_VELOCIDAD, MAX_VELOCIDAD
from random import uniform
from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class FantasmaVertical(QObject):
    senal_mover = pyqtSignal(int)

    def __init__(self, posicion: tuple, id: int) -> None:
        super().__init__()
        self.posicion = posicion
        self.id = id
        self.instalar_timer()
        self.vivo = True
        self.nombre = "fantasma_vertical"
        self.direccion_inicio = "w"
        self.direccion_movimiento = "w"

    def instalar_timer(self) -> None:
        """Instala el timer del movimiento del fantasma"""
        self.ponderador = uniform(MIN_VELOCIDAD, MAX_VELOCIDAD)
        self.tiempo_movimiento = int((1 / self.ponderador) * 1000)  # En ms
        self.timer_movimiento_fantasma = QTimer()
        self.timer_movimiento_fantasma.setInterval(self.tiempo_movimiento)
        self.timer_movimiento_fantasma.timeout.connect(
            self.solicitar_movimiento)

    def iniciar_movimiento(self) -> None:
        """Inicializa el timer del movimiento"""
        self.timer_movimiento_fantasma.start()

    def detener_movimiento(self) -> None:
        """Detiene el timer del movimiento"""
        self.timer_movimiento_fantasma.stop()

    def solicitar_movimiento(self) -> None:
        """Mueve el fantasma"""
        self.senal_mover.emit(self.id)

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion

    def cambiar_direccion(self) -> str:
        """Cambia y retorna la nueva dirección"""
        if self.direccion_movimiento == "w":
            self.direccion_movimiento = "s"
        elif self.direccion_movimiento == "s":
            self.direccion_movimiento = "w"
        return self.direccion_movimiento


class FantasmaHorizontal(QObject):
    senal_mover = pyqtSignal(int)

    def __init__(self, posicion: tuple, id: int) -> None:
        super().__init__()
        self.posicion = posicion
        self.id = id
        self.instalar_timer()
        self.vivo = True
        self.nombre = "fantasma_horizontal"
        self.direccion_inicio = "d"
        self.direccion_movimiento = "d"

    def instalar_timer(self) -> None:
        """Instala el timer del movimiento del fantasma"""
        self.ponderador = uniform(MIN_VELOCIDAD, MAX_VELOCIDAD)
        self.tiempo_movimiento = int((1 / self.ponderador) * 1000)  # En ms
        self.timer_movimiento_fantasma = QTimer()
        self.timer_movimiento_fantasma.setInterval(self.tiempo_movimiento)
        self.timer_movimiento_fantasma.timeout.connect(
            self.solicitar_movimiento)

    def iniciar_movimiento(self) -> None:
        """Inicializa el timer del movimiento"""
        self.timer_movimiento_fantasma.start()

    def detener_movimiento(self) -> None:
        """Detiene el timer del movimiento"""
        self.timer_movimiento_fantasma.stop()

    def solicitar_movimiento(self) -> None:
        """Mueve el fantasma"""
        self.senal_mover.emit(self.id)

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion

    def cambiar_direccion(self) -> str:
        """Cambia y retorna la nueva dirección"""
        if self.direccion_movimiento == "d":
            self.direccion_movimiento = "a"
        elif self.direccion_movimiento == "a":
            self.direccion_movimiento = "d"
        return self.direccion_movimiento


class FantasmaFollowerVillain(QObject):
    senal_mover = pyqtSignal(int)

    def __init__(self, posicion: tuple, id: int) -> None:
        super().__init__()
        self.posicion = posicion
        self.id = id
        self.instalar_timer()
        self.vivo = True
        self.nombre = "fantasma_followervillain"
        self.direccion_inicio = "d"
        self.direccion_movimiento = "d"

    def instalar_timer(self) -> None:
        """Instala el timer del movimiento del fantasma"""
        self.ponderador = uniform(MIN_VELOCIDAD, MAX_VELOCIDAD)
        self.tiempo_movimiento = int((1 / self.ponderador) * 1000)  # En ms
        self.timer_movimiento_fantasma = QTimer()
        self.timer_movimiento_fantasma.setInterval(self.tiempo_movimiento)
        self.timer_movimiento_fantasma.timeout.connect(
            self.solicitar_movimiento)

    def iniciar_movimiento(self) -> None:
        """Inicializa el timer del movimiento"""
        self.timer_movimiento_fantasma.start()

    def detener_movimiento(self) -> None:
        """Detiene el timer del movimiento"""
        self.timer_movimiento_fantasma.stop()

    def solicitar_movimiento(self) -> None:
        """Mueve el fantasma"""
        self.senal_mover.emit(self.id)

    def actualizar_posicion(self, nueva_posicion: tuple) -> None:
        """Actualiza el self.posicion"""
        self.posicion = nueva_posicion

    def cambiar_direccion(self) -> str:
        """Cambia y retorna la nueva dirección"""
        if self.direccion_movimiento == "d":
            self.direccion_movimiento = "a"
        elif self.direccion_movimiento == "a":
            self.direccion_movimiento = "d"
        elif self.direccion_movimiento == "w":
            self.direccion_movimiento = "s"
        elif self.direccion_movimiento == "s":
            self.direccion_movimiento = "w"
        return self.direccion_movimiento

    def definir_direccion(self, posicion_luigi: tuple,
                          posiciones_bloqueadas: set) -> None:
        """Actualiza la dirección dependiendo
        de la posición en la que esté Luigi"""
        posiciones = {}
        posiciones["w"] = auxiliar.obtener_nueva_posicion("w", self.posicion)
        posiciones["a"] = auxiliar.obtener_nueva_posicion("a", self.posicion)
        posiciones["s"] = auxiliar.obtener_nueva_posicion("s", self.posicion)
        posiciones["d"] = auxiliar.obtener_nueva_posicion("d", self.posicion)
        direccion_escogida = "w"  # Default
        minima_distancia = None
        for direccion in posiciones:
            posible_posicion = posiciones[direccion]
            if posible_posicion not in posiciones_bloqueadas:
                distancia = auxiliar.obtener_distancia_casillas(
                    posiciones[direccion], posicion_luigi)
                if auxiliar.casilla_alcanzable(self.posicion, direccion,
                                               posicion_luigi,
                                               posiciones_bloqueadas):
                    if minima_distancia is None or distancia < minima_distancia:
                        minima_distancia = distancia
                        direccion_escogida = direccion
        self.direccion_movimiento = direccion_escogida
