from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap, QKeyEvent
from parametros import PATH_FONDO, PATH_LOGO, DIMENSIONES_VENTANA_INICIO, \
    TITULO_VENTANA_INICIO, PONDERACION_DIMENSIONES_FONDO, POSICION_VENTANAS
import os
import auxiliares as auxiliar


class VentanaInicio(QWidget):
    senal_registar_inicio = pyqtSignal(str, int)

    def __init__(self) -> None:
        super().__init__()
        self.inicializa_gui()

    def inicializa_gui(self) -> None:
        """Inicializa los elementos del GUI"""
        self.titulo_ventana = TITULO_VENTANA_INICIO
        self.setGeometry(*POSICION_VENTANAS, *DIMENSIONES_VENTANA_INICIO)
        self.setWindowTitle(self.titulo_ventana)

        # Inicializar fondos, widgets, estilización
        self.instalar_fondo()
        self.instalar_widgets()
        self.agregar_estilo()
        self.conectar_botones()
        
    def instalar_fondo(self) -> None:
        """Instancia el fondo"""
        self.background = QLabel(self)
        path_fondo = os.path.join(*PATH_FONDO)
        self.background.setPixmap(QPixmap(path_fondo))
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.background.setScaledContents(True)
        self.dimensiones_fondo = (int(600 * PONDERACION_DIMENSIONES_FONDO),
                                  int(680 * PONDERACION_DIMENSIONES_FONDO))
        self.background.setGeometry(0, -150, *self.dimensiones_fondo)

    def instalar_widgets(self) -> None:
        """Agrega los widgets al layout"""
        # Creación del Layout
        layout = QVBoxLayout()
        layout_username = QHBoxLayout()
        layout_selector = QHBoxLayout()

        # Definición de self.texto_login, etc..
        self.logo_juego = self.instanciar_logo()
        self.texto_login = self.instanciar_texto_login()
        self.input_login = self.instanciar_input_login()
        self.boton_exit = self.instanciar_boton_exit()
        self.selector_mapas = self.instanciar_selector_mapas()
        self.boton_login = self.instanciar_boton_ingreso()

        # Agregar widgets a los respectivos Layouts y agruparlos
        layout_username.addWidget(self.texto_login)
        layout_username.addWidget(self.input_login)
        layout_selector.addWidget(self.selector_mapas)
        layout_selector.addWidget(self.boton_login)
        layout.addWidget(self.logo_juego)
        layout.addLayout(layout_username)
        layout.addLayout(layout_selector)
        layout.addStretch(4)
        layout.addWidget(self.boton_exit)
        self.setLayout(layout)

    def instanciar_logo(self) -> object:
        """Instancia y retorna QLabel del logo"""
        logo_juego = QLabel(self)
        path_logo_juego = os.path.join(*PATH_LOGO)
        logo_juego.setPixmap(QPixmap(path_logo_juego))
        logo_juego.setAttribute(Qt.WA_TransparentForMouseEvents)
        logo_juego.setScaledContents(True)
        return logo_juego

    def instanciar_texto_login(self) -> object:
        """Instancia y retorna el texto del login"""
        texto_login = QLabel('Nombre: ', self)
        return texto_login

    def instanciar_input_login(self) -> object:
        """Instancia y retorna el input del login"""
        input_usuario = QLineEdit('', self)
        input_usuario.setPlaceholderText("Ingrese nombre de usuario")
        return input_usuario

    def instanciar_selector_mapas(self) -> object:
        """Instancia y retorna el selector de mapas"""
        selector_mapas = QComboBox(self)
        selector_mapas.addItem('Construir mapa', 0)
        mapas = auxiliar.obtener_mapas()
        for mapa in mapas:
            selector_mapas.addItem(mapas[mapa], mapa)
        return selector_mapas

    def instanciar_boton_ingreso(self) -> object:
        """Instancia y retorna el botón de inicio"""
        boton_login = QPushButton("Ingresar", self)
        return boton_login
    
    def instanciar_boton_exit(self) -> object:
        """Instancia y retorna botón de exit"""
        boton_exit = QPushButton("Salir del programa", self)
        return boton_exit

    def agregar_estilo(self) -> None:
        """Agrega estilo al texto del login"""
        self.texto_login.setStyleSheet(
            """
            color:white;
        """
        )

    def conectar_botones(self) -> None:
        """Conecta los botones de ingreso y exit"""
        self.boton_exit.clicked.connect(self.close)
        self.boton_login.clicked.connect(self.enviar_info)

    def enviar_info(self) -> None:
        """Notifica al backend los datos
        para empezar el juego"""
        # Le avisamos al backend la dificultad y el nombre mediante la señal.
        nombre = self.input_login.text()
        index_selector = self.selector_mapas.currentIndex()
        valor_selector = self.selector_mapas.itemData(index_selector)
        self.senal_registar_inicio.emit(nombre, valor_selector)

    def alertar(self, texto: str) -> None:
        """Levanta una alerta con contenido 'texto'"""
        auxiliar.alertar(texto, "warning")

    # BONUS: detectar cuando se presiona enter para también enviar_info
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Intenta comenzar el juego presionando enter"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.enviar_info()
