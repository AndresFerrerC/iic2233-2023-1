from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QTimer


class Temporizador(QLabel):
    senal_termino_temporizador = pyqtSignal()

    def __init__(self, parent: object, tiempo: int) -> None:
        super().__init__(parent)
        self.tiempo_inicial = tiempo
        self.tiempo_restante = tiempo
        self.instalar_temporizador()
        self.comenzar_temporizador()
        self.setText(self.formatear_tiempo(self.tiempo_restante))

    def instalar_temporizador(self) -> None:
        """Instancia el timer para la cuenta regresiva"""
        self.timer_temporizador = QTimer()
        self.timer_temporizador.setInterval(1000)
        self.timer_temporizador.timeout.connect(self.actualizar_temporizador)

    def comenzar_temporizador(self) -> None:
        """Comienza el temporizador"""
        self.timer_temporizador.start()

    def detener_temporizador(self) -> None:
        """Detiene el temporizador"""
        self.timer_temporizador.stop()

    def actualizar_temporizador(self) -> None:
        """Actualiza el valor temporizador"""
        self.tiempo_restante -= 1
        if self.tiempo_restante == 0:
            # Enviar señal de término
            self.senal_termino_temporizador.emit()
            self.detener_temporizador()
        self.setText(self.formatear_tiempo(self.tiempo_restante))

    def hackear_tiempo(self) -> None:
        """Detiene el temporizador y establece
        tiempo en su valor por defecto"""
        self.tiempo_restante = self.tiempo_inicial
        self.detener_temporizador()

    def reiniciar_tiempo(self) -> None:
        """Reestablece el tiempo restante
        y reinicia el contador"""
        self.tiempo_restante = self.tiempo_inicial
        self.comenzar_temporizador()

    def formatear_tiempo(self, segundos: int) -> str:
        """Devuelve la cantidad de segundos en formato mm:ss"""
        min_restantes = segundos // 60
        seg_restantes = segundos % 60
        tiempo_formateado = f'Tiempo: {min_restantes:02}:{seg_restantes:02}'
        return tiempo_formateado
