from PyQt5.QtCore import QObject, pyqtSignal
from parametros import MIN_CARACTERES, MAX_CARACTERES


class Inicio(QObject):
    senal_empezar_juego = pyqtSignal()
    senal_alertar_inicio = pyqtSignal(str)
    senal_abrir_juego = pyqtSignal(str, int)

    def __init__(self) -> None:
        super().__init__()
        self.nombre_jugador = None
        self.mapa_escogido = None

    def registrar_inicio(self, nombre: str, mapa: int) -> None:
        if len(nombre) == 0:
            self.senal_alertar_inicio.emit("El nombre no puede estar vacío :C")
        elif not nombre.isalnum():
            self.senal_alertar_inicio.emit("El nombre no es alfanumérico UnU")
        elif len(nombre) > MAX_CARACTERES or len(nombre) < MIN_CARACTERES:
            self.senal_alertar_inicio.emit(f"El nombre debe contener entre"
                                           f" {MIN_CARACTERES} y"
                                           f" {MAX_CARACTERES} caracteres D:")
        elif len([letra for letra in nombre.lower()
                  if letra in ["á", "é", "í", "ó", "ú"]]) > 0:  # Hay tildes
            self.senal_alertar_inicio.emit("El nombre no puede tener tildes")
        else:
            self.nombre_jugador = nombre
            self.mapa_escogido = mapa
            self.iniciar_juego()

    def iniciar_juego(self) -> None:
        """Avisa al frontend el inicio del juego"""
        self.senal_empezar_juego.emit()
        self.senal_abrir_juego.emit(self.nombre_jugador,
                                    self.mapa_escogido)
