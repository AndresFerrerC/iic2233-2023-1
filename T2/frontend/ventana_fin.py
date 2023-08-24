from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from parametros import PATH_LOGO, DIMENSIONES_VENTANA_FIN, POSICION_VENTANAS
import frontend.reproductor as reproductor
import os


class VentanaFin(QWidget):
    senal_reiniciar_backend = pyqtSignal()
    senal_reiniciar_frontend = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.inicializa_gui() 
        self.reproductor = reproductor.Reproductor(self)

    def inicializa_gui(self) -> None:
        """Inicializa los elementos visuales"""
        self.titulo_ventana = "Fin del juego" 
        self.setGeometry(*POSICION_VENTANAS, *DIMENSIONES_VENTANA_FIN)
        self.setWindowTitle(self.titulo_ventana)
        self.instalar_widgets()
        self.agregar_estilo()
        self.conectar_botones()

    def instalar_widgets(self) -> None:
        """Agrega los widgets al layout"""
        # Creación del Layout
        layout = QVBoxLayout()
        layout_botones = QHBoxLayout()

        # Definición de self.logo_juego, etc.
        self.logo_juego = self.instanciar_logo()
        self.texto_estado = self.instanciar_texto_estado()
        self.texto_vidas = self.instanciar_texto_vidas()
        self.texto_puntaje = self.instanciar_texto_puntaje()
        self.boton_salir = self.instanciar_boton_salir()
        self.boton_jugar = self.instanciar_boton_jugar()
        self.estilizar_botones()
        # Agregar widgets a los respectivos Layouts y agruparlos
        layout.addWidget(self.logo_juego)
        layout.addWidget(self.texto_estado)
        layout.addWidget(self.texto_vidas)
        layout.addWidget(self.texto_puntaje)
        layout_botones.addWidget(self.boton_jugar)
        layout_botones.addWidget(self.boton_salir)
        layout.addLayout(layout_botones)
        self.setLayout(layout)

    def instanciar_logo(self) -> object:
        """Instancia y retorna QLabel del logo"""
        logo_juego = QLabel(self)
        path_logo_juego = os.path.join(*PATH_LOGO)
        logo_juego.setPixmap(QPixmap(path_logo_juego))
        logo_juego.setAttribute(Qt.WA_TransparentForMouseEvents)
        logo_juego.setScaledContents(True)
        return logo_juego

    def agregar_estilo(self) -> None:
        """Agrega estilo al fondo"""
        self.setStyleSheet(
            """
            background-color: #1f1f1f;
            color:white;
        """
        )
    
    def estilizar_botones(self) -> None:
        """Evita que los botones adquieran
        el color de fondo de la ventana"""
        self.boton_jugar.setStyleSheet(
            """
            background-color: #568A37;
        """
        )
        self.boton_salir.setStyleSheet(
            """
            background-color: #AE554C;
        """
        )

    def instanciar_texto_estado(self) -> object:
        """Instancia y retorna el label del estado"""
        texto_estado = QLabel('Estado', self)
        return texto_estado

    def instanciar_texto_vidas(self) -> object:
        """Instancia y retorna el label de las vidas"""
        texto_vidas = QLabel('Tiempo', self)
        return texto_vidas

    def instanciar_texto_puntaje(self) -> object:
        """Instancia y retorna el texto del puntaje"""
        texto_puntaje = QLabel('Puntaje', self)
        return texto_puntaje

    def instanciar_boton_salir(self) -> object:
        """Instancia y retorna botón de exit"""
        boton_exit = QPushButton("Salir del juego", self)
        return boton_exit

    def instanciar_boton_jugar(self) -> object:
        """Instancia y retorna botón de jugar de nuevo"""
        boton_jugar = QPushButton("Jugar de nuevo", self)
        return boton_jugar

    def conectar_botones(self) -> None:
        """Conecta los botones de ingreso y exit"""
        self.boton_salir.clicked.connect(self.close)
        self.boton_jugar.clicked.connect(self.reiniciar_partida)

    def mostrar_ventana(self, datos: dict) -> None:
        """Muestra la ventana de fin.
        Requiere de los datos de la partida"""
        self.show()
        self.texto_estado.setText(datos["texto_estado"])
        self.texto_puntaje.setText(datos["texto_puntaje"])
        self.texto_vidas.setText(datos["texto_vidas"])
        self.reproductor.reproducir_audio(datos["estado"])

    def reiniciar_partida(self) -> None:
        """Notifica al frontend y al backend del reinicio"""
        self.senal_reiniciar_frontend.emit()
        self.senal_reiniciar_backend.emit()
        self.hide()
