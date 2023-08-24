from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
import os
import auxiliares as auxiliar
import frontend.iconos as iconos


class VentanaInicio(QWidget):
    senal_registar_inicio = pyqtSignal()
    path_parametros = "parametros.json"
    parametros = auxiliar.leer_archivo_json(path_parametros)

    def __init__(self) -> None:
        super().__init__()
        self.inicializa_gui()

    def inicializa_gui(self) -> None:
        """Inicializa los elementos del GUI"""
        self.titulo_ventana = self.parametros["titulo_ventana_inicio"]
        self.posicion_ventana = self.parametros["posiciones_ventanas"]
        self.dimensiones_ventana = self.parametros["dimensiones_ventanas"]

        # Dimensiones y título
        self.setGeometry(*self.posicion_ventana, *self.dimensiones_ventana)
        self.setWindowTitle(self.titulo_ventana)
        self.setMaximumWidth(self.dimensiones_ventana[0])
        self.setMaximumHeight(self.dimensiones_ventana[1])

        # Inicializar fondos, widgets, estilización
        self.instalar_fondo()
        self.instalar_widgets()
        self.conectar_botones()

    def instalar_fondo(self) -> None:
        """Instancia el fondo"""
        ubicacion_fondo = self.parametros["path_background"] + \
            [self.parametros["imagenes_background"]["inicio"]]

        self.background = QLabel(self)
        path_fondo = os.path.join(*ubicacion_fondo)
        self.background.setPixmap(QPixmap(path_fondo))
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.background.setScaledContents(True)
        self.dimensiones_fondo = (700, 520)
        self.background.setGeometry(0, 0, *self.dimensiones_fondo)

    def instalar_widgets(self) -> None:
        """Agrega los widgets al layout"""
        # Creación del layout
        layout = QVBoxLayout()
        layout_espera = QHBoxLayout()
        layout_espera.setAlignment(Qt.AlignHCenter)

        # Creación de los widgets
        self.boton_exit = self.instanciar_boton_exit()
        self.boton_login = self.instanciar_boton_ingreso()
        self.texto_inicio = self.instanciar_texto_inicio()
        self.estilizar_botones()

        # Creación de las imagenes y el texto de users
        self.instalar_usuarios()

        # Agregar widgets a los respectivos layouts
        layout_espera.addWidget(self.texto_inicio)
        layout.addLayout(layout_espera)
        layout.addStretch(4)
        layout.addWidget(self.boton_login)
        layout.addWidget(self.boton_exit)
        self.setLayout(layout)

    def instalar_usuarios(self) -> None:
        """Instancia los labels de los usuarios
        y sus respectivos input para los textos"""
        self.iconos = {}
        self.usuarios = {}
        for i in range(4):  # <-- LISTA_USUARIOS
            posicion_icon = (70 + i * 150, 150)
            posicion_texto = (70 + i * 150, 255)
            self.iconos[i + 1] = iconos.Usuario(self, posicion_icon)
            self.iconos[i + 1].show()
            self.usuarios[i + 1] = QLabel('Cargando...', self)
            self.usuarios[i + 1].setAlignment(Qt.AlignCenter)
            self.usuarios[i + 1].move(*posicion_texto)
            self.agregar_estilo(self.usuarios[i + 1], "texto")
        self.agregar_estilo(self.texto_inicio, "titular")

    def instanciar_texto_inicio(self) -> object:
        """Instancia el texto del inicio"""
        texto_inicio = QLabel("Sala de Espera", self)
        return texto_inicio

    def instanciar_boton_ingreso(self) -> object:
        """Instancia y retorna el botón de inicio"""
        boton_login = QPushButton("Jugar", self)
        boton_login.setEnabled(False)  # Por defecto
        return boton_login

    def instanciar_boton_exit(self) -> object:
        """Instancia y retorna botón de exit"""
        boton_exit = QPushButton("Salir", self)
        return boton_exit

    def agregar_estilo(self, objeto: object, tipo: str) -> None:
        """Agrega estilo al objeto.
        Si es titulo, tamaño 22px. Otro caso, 15px"""
        if tipo == "titular":
            objeto.setStyleSheet(
                """
                color:white; font-size:22px;
             """
            )
        elif tipo == "personaje":
            objeto.setStyleSheet(
                """
                color:white; font-size:15px;
                background-color:#2F87E8; 
                border: 1px solid white;
                border-radius: 10px;

            """
            )
        else:
            objeto.setStyleSheet(
                """
                color:white; font-size:15px;
            """
            )

    def conectar_botones(self) -> None:
        """Conecta los botones de ingreso y login"""
        self.boton_exit.clicked.connect(self.cerrar)
        self.boton_login.clicked.connect(self.jugar)

    def estilizar_botones(self) -> None:
        """Agrega estilo a los botones"""
        self.boton_login.setStyleSheet(
            """
            background-color: #63A6FC;
        """
        )
        self.boton_exit.setStyleSheet(
            """
            background-color: #AE554C;
        """
        )

    def actualizar_frontend(self, datos: dict) -> None:
        """Actualiza los datos del frontend"""
        habilitado = datos["habilitado_jugar"]
        dict_jugadores = datos["jugadores"]
        id_asignado = datos["jugador_asignado"]
        self.actualizar_boton_jugar(habilitado)
        self.actualizar_jugadores(dict_jugadores, id_asignado)

    def actualizar_jugadores(self, jugadores: dict, asignado: str) -> None:
        """Actualiza los jugadores"""
        for id_jugador in jugadores:
            nombre = jugadores[id_jugador]
            self.usuarios[id_jugador].setText(nombre)
            if asignado != "Undefined":
                self.agregar_estilo(self.usuarios[asignado], "personaje")

    def actualizar_boton_jugar(self, estado: bool) -> None:
        """Actualiza el estado del botón jugar"""
        self.boton_login.setEnabled(estado)

    def jugar(self) -> None:
        """Notifica al backend para iniciar el juego"""
        self.senal_registar_inicio.emit()

    def cerrar(self) -> None:
        """Cierra la ventana"""
        self.close()
