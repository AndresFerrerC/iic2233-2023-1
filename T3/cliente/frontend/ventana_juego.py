from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPixmap, QKeyEvent
from collections import defaultdict
import os
import auxiliares as auxiliar
import frontend.iconos as iconos


class VentanaJuego(QWidget):
    # Señales
    senal_anunciar_valor = pyqtSignal(str)
    senal_pasar_turno = pyqtSignal()
    senal_dudar = pyqtSignal()
    senal_cambiar_dados = pyqtSignal()
    senal_usar_poder = pyqtSignal()
    senal_aplicar_poder = pyqtSignal(int)

    # Parámetros
    path_parametros = "parametros.json"
    parametros = auxiliar.leer_archivo_json(path_parametros)

    def __init__(self) -> None:
        super().__init__()
        self.inicializa_gui()

    def inicializa_gui(self) -> None:
        """Inicializa los elementos del GUI"""
        self.titulo_ventana = self.parametros["titulo_ventana_juego"]
        self.posicion_ventana = self.parametros["posiciones_ventanas"]
        self.dimensiones_ventana = self.parametros["dimensiones_ventanas"]
        self.habilitado_dudar_teclas = False
        self.usuarios_habilitados_dudar = {}
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
            [self.parametros["imagenes_background"]["juego"]]

        self.background = QLabel(self)
        path_fondo = os.path.join(*ubicacion_fondo)
        self.background.setPixmap(QPixmap(path_fondo))
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.background.setScaledContents(True)
        self.dimensiones_fondo = (700, 520)
        self.background.setGeometry(0, 0, *self.dimensiones_fondo)

    def instalar_widgets(self) -> None:
        """Instala los elementos gráficos
        que son actualizados por el cliente/servidor"""
        # Textos del status del juego
        self.textos = self.instanciar_textos()
        # Creación de las imagenes y el texto de users
        self.instalar_usuarios()
        # Creación de los botones de partida y label
        self.instalar_botones()
        self.instalar_input()

    def instalar_usuarios(self) -> None:
        """Instancia los labels de los usuarios
        y sus respectivos input para los textos"""
        self.iconos = {}
        self.usuarios = {}
        self.dados = defaultdict(list)
        self.vidas = {}
        # Las posiciones no deben ser modificadas.
        posiciones_iconos = {1: (320, 360), 2: (120, 200),
                             3: (320, 60), 4: (500, 200)}
        posiciones_nombre = {1: (295, 435), 2: (90, 280),
                             3: (295, 130), 4: (500, 280)}
        posiciones_dados = {1: [(310, 310), (360, 310)], 2: [(220, 200), (220, 250)],
                            3: [(310, 165), (360, 165)], 4: [(450, 200), (450, 250)]}
        posiciones_vidas = {1: (400, 380), 2: (70, 220),
                            3: (400, 80), 4: (580, 220)}
        for i in range(1, self.parametros["numero_jugadores"] + 1):
            posicion_icon = posiciones_iconos[i]
            self.iconos[i] = iconos.Usuario(self, posicion_icon, 0.7)
            # Instalar los dados en las posiciones respectivas
            for posicion in posiciones_dados[i]:
                self.dados[i].append(iconos.Dado(self, posicion, -2))

            self.vidas[i] = iconos.Dado(self, posiciones_vidas[i], -1)
            self.usuarios[i] = QLabel(f'Jugador {i}', self)
            self.usuarios[i].setGeometry(*posiciones_nombre[i], 120, 30)
            self.usuarios[i].setAlignment(Qt.AlignCenter)
            self.agregar_estilo(self.usuarios[i], "nombre")

    def instanciar_textos(self) -> dict:
        """Retorna un diccionario con los textos instanciados"""
        diccionario_textos = {}
        diccionario_textos["turno_actual"] = self.instanciar_turno()
        diccionario_textos["turno_anterior"] = self.instanciar_turno_anterior()
        diccionario_textos["numero_mayor"] = self.instanciar_numero_mayor()
        diccionario_textos["numero_turno"] = self.instanciar_numero_turno()
        return diccionario_textos

    def instanciar_turno(self) -> object:
        """Instancia el texto del turno actual"""
        texto_turno = QLabel("Turno de: [Cargando]", self)
        texto_turno.setAlignment(Qt.AlignCenter)
        texto_turno.setGeometry(250, 0, 200, 20)
        self.agregar_estilo(texto_turno, "otro")
        return texto_turno

    def instanciar_turno_anterior(self) -> object:
        """Instancia el texto del turno anterior"""
        texto_turno = QLabel("Turno anterior fue: [Cargando]", self)
        texto_turno.setAlignment(Qt.AlignCenter)
        texto_turno.setGeometry(235, 30, 250, 20)
        self.agregar_estilo(texto_turno, "otro")
        return texto_turno

    def instanciar_numero_mayor(self) -> object:
        """Instancia el texto del número mayor"""
        texto_numero = QLabel("Número mayor anunciado: [X]", self)
        texto_numero.setAlignment(Qt.AlignCenter)
        texto_numero.setGeometry(25, 30, 200, 20)
        self.agregar_estilo(texto_numero, "otro")
        return texto_numero

    def instanciar_numero_turno(self) -> object:
        """Instancia el texto del número de turno"""
        texto_numero_turno = QLabel("Número turno: [Cargando]", self)
        texto_numero_turno.setAlignment(Qt.AlignCenter)
        texto_numero_turno.setGeometry(500, 30, 200, 20)
        self.agregar_estilo(texto_numero_turno, "otro")
        return texto_numero_turno

    def instalar_botones(self) -> None:
        """Crea los botones de la partida"""
        self.btn_posiciones = {"Anunciar valor": (450, 380),
                               "Pasar turno": (450, 420),
                               "Usar poder": (450, 460),
                               "Cambiar dados": (570, 420),
                               "Dudar": (570, 460)}
        self.botones = {}
        for nombre_boton in self.btn_posiciones:
            self.botones[nombre_boton] = QPushButton(nombre_boton, self)
            self.botones[nombre_boton].setGeometry(
                *self.btn_posiciones[nombre_boton], 120, 40)
            self.agregar_estilo(self.botones[nombre_boton], "boton")
            self.botones[nombre_boton].setEnabled(False)  # Por defecto
        self.agregar_estilo(self.botones["Anunciar valor"], "boton_main")

    def instalar_input(self) -> None:
        """Instala el QLineEdit para ingresar el valor"""
        posicion_input = (570, 380)
        self.input_valor = QLineEdit("", self)
        self.input_valor.setPlaceholderText("Espera tu turno...")
        self.input_valor.setGeometry(*posicion_input, 120, 40)
        self.input_valor.setEnabled(False)

    def agregar_estilo(self, objeto: object, tipo: str) -> None:
        """Agrega estilo al objeto. Puede ser nombre, personaje (jugador),
        muerto (para personajes muertos), boton u otros. """
        if tipo == "nombre":
            objeto.setStyleSheet(
                """
                color:white; font-size:16px;
                """
            )
        elif tipo == "muerto":  # Para jugadores retirados
            objeto.setStyleSheet(
                """
                color:red; font-size:16px;
                """
            )
        elif tipo == "personaje":
            objeto.setStyleSheet(
                """
                color:white; font-size:16px;
                background-color:green; 
                border: 1px solid white;
                border-radius: 10px;

                """
            )
        elif tipo == "boton":
            objeto.setStyleSheet(
                """
                background-color: #215196; color:white;
                """
            )
        elif tipo == "bot":
            objeto.setStyleSheet(
                """
                color:white; font-size:16px;
                background-color:#483D35;
                border: 0.5px solid white;
                border-radius: 10px;
                """
            )
        elif tipo == "boton_main":
            objeto.setStyleSheet(
                """
                background-color: #377EC6; color:white;
                """
            )
        else:
            objeto.setStyleSheet(
                """
                color:white; font-size:14px;
                """
            )

    def conectar_botones(self) -> None:
        """Conecta los botones del juego"""
        self.botones["Anunciar valor"].clicked.connect(self.anunciar_valor)
        self.botones["Pasar turno"].clicked.connect(self.pasar_turno)
        self.botones["Dudar"].clicked.connect(self.dudar)
        self.botones["Cambiar dados"].clicked.connect(self.cambiar_dados)
        self.botones["Usar poder"].clicked.connect(self.usar_poder)

    def anunciar_valor(self) -> None:
        """Notifica al backend que quiere anunciar valor"""
        valor_a_anunciar = self.input_valor.text()
        self.senal_anunciar_valor.emit(valor_a_anunciar)

    def pasar_turno(self) -> None:
        """Notifica al backend que quiere pasar turno"""
        self.senal_pasar_turno.emit()

    def dudar(self) -> None:
        """Notifica al backend que se duda"""
        self.senal_dudar.emit()

    def cambiar_dados(self) -> None:
        """Solicita al backend cambiar dados"""
        self.senal_cambiar_dados.emit()

    def usar_poder(self) -> None:
        """Notifica al backend el uso de poder"""
        self.senal_usar_poder.emit()

    def actualizar_frontend(self, datos: dict) -> None:
        """Actualiza los datos del frontend"""
        # Obtener datos del diccionario
        dict_habilitado = datos["habilitado"]
        turno_actual = datos["turno"]
        turno_anterior = datos["turno_anterior"]
        numero_mayor = datos["numero_mayor"]
        numero_turno = datos["numero_turno"]
        dict_jugadores = datos["jugadores"]
        id_asignado = datos["jugador_asignado"]
        lista_bots = datos["lista_bots"]
        dados = datos["dados"]
        vidas = datos["vidas"]
        # Interpretación
        self.actualizar_habilitado_jugar(dict_habilitado)
        self.actualizar_jugadores(dict_jugadores, id_asignado, lista_bots)
        self.actualizar_textos(turno_actual, turno_anterior, numero_turno,
                               numero_mayor)
        self.actualizar_dados(dados)
        self.actualizar_vidas(vidas)

    def actualizar_jugadores(self, jugadores: dict, asignado: str,
                             lista_bots: list) -> None:
        """Actualiza los jugadores"""
        for id_jugador in jugadores:
            nombre = jugadores[id_jugador]
            self.usuarios[id_jugador].setText(nombre)
            self.agregar_estilo(self.usuarios[asignado], "personaje")
        for id_bot in lista_bots:
            self.agregar_estilo(self.usuarios[id_bot], "bot")

    def actualizar_habilitado_jugar(self, estado: dict) -> None:
        """Actualiza el estado de los botones"""
        habilitado_turno = estado["turno"]
        habilitado_dudar = estado["dudar"]
        habilitado_poder = estado["poder"]
        habilitado_cambiar = estado["cambiar"]
        self.usuarios_habilitados_dudar = estado["dudar_teclas"]
        self.botones["Anunciar valor"].setEnabled(habilitado_turno)
        self.botones["Pasar turno"].setEnabled(habilitado_turno)
        self.botones["Dudar"].setEnabled(habilitado_dudar)
        self.botones["Cambiar dados"].setEnabled(habilitado_cambiar)
        self.botones["Usar poder"].setEnabled(habilitado_poder)
        self.input_valor.setEnabled(habilitado_turno)
        if habilitado_turno:
            self.input_valor.clear()
            self.input_valor.setPlaceholderText("¡Ingresa el valor!")
        else:
            self.input_valor.clear()
            self.input_valor.setPlaceholderText("Espera tu turno...")
        if self.usuarios_habilitados_dudar is not None:
            self.habilitado_dudar_teclas = True
        else:
            self.habilitado_dudar_teclas = False

    def actualizar_dados(self, dados: dict) -> None:
        """Actualiza los dados"""
        for id_jugador in dados:
            dados_jugador = dados[id_jugador]
            for i in range(len(dados_jugador)):
                dado = dados_jugador[i]
                self.dados[id_jugador][i].actualizar_valor(dado)

    def actualizar_vidas(self, vidas: dict) -> None:
        """Actualiza las vidas"""
        for id_jugador in vidas:
            vidas_jugador = vidas[id_jugador]
            self.vidas[id_jugador].actualizar_valor(vidas_jugador)

    def actualizar_textos(self, actual: str, anterior: str,
                          turno: str, mayor: str) -> None:
        """Actualiza los textos de turno actual, anterior, etc."""
        self.textos["turno_actual"].setText(f"Turno de: {actual}")
        self.textos["turno_anterior"].setText(f"Turno anterior fue:"
                                              f" {anterior}")
        self.textos["numero_mayor"].setText(f"Número mayor anunciado: {mayor}")
        self.textos["numero_turno"].setText(f"Número turno: {turno}")

    def cerrar(self) -> None:
        """Cierra la ventana"""
        self.close()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Utiliza un poder"""
        if self.habilitado_dudar_teclas:
            if event.key() == Qt.Key_W:
                if self.usuarios_habilitados_dudar[3]:
                    self.senal_aplicar_poder.emit(3)
            elif event.key() == Qt.Key_A:
                if self.usuarios_habilitados_dudar[2]:
                    self.senal_aplicar_poder.emit(2)
            elif event.key() == Qt.Key_S:
                if self.usuarios_habilitados_dudar[1]:
                    self.senal_aplicar_poder.emit(1)
            elif event.key() == Qt.Key_D:
                if self.usuarios_habilitados_dudar[4]:
                    self.senal_aplicar_poder.emit(4)
