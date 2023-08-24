from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QShortcut
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QKeyEvent, QKeySequence
from parametros import TITULO_VENTANA_JUEGO, DIMENSIONES_VENTANA_JUEGO, \
    POSICION_VENTANAS, TIEMPO_CUENTA_REGRESIVA, ANCHO_GRILLA, LARGO_GRILLA, \
    DIMENSION_SPRITES
from frontend.drag_and_drop import BotonMovible
import frontend.temporizador as temporizador
import auxiliares as auxiliar
import frontend.frontend_objetos as objetos
from frontend.frontend_luigi import Luigi


class VentanaJuego(QWidget):
    # Señales del constructor
    senal_mostrar_items = pyqtSignal(int)
    senal_agregar_items = pyqtSignal(str, int, int)
    senal_limpiar_grilla = pyqtSignal()
    senal_intentar_jugar = pyqtSignal()
    
    # Señales del juego
    senal_mover_personaje = pyqtSignal(str)
    senal_fin_tiempo = pyqtSignal()
    senal_solicitar_pausa = pyqtSignal(bool)
    senal_solicitar_ganar = pyqtSignal()
    senal_enviar_tiempo = pyqtSignal(int)
    senal_matar_fantasmas = pyqtSignal()
    senal_vida_infinita = pyqtSignal()

    def __init__(self) -> None:
        # Ventana oculta por defecto
        super().__init__()
        self.inicializa_gui()
        self.item_seleccionado = None
        self.juego_iniciado = False
        self.modo_juego = "constructor"

    def inicializa_gui(self) -> None:
        """Inicializa los elementos de la ventana"""
        self.titulo_ventana = TITULO_VENTANA_JUEGO
        self.setAcceptDrops(True)
        self.setGeometry(*POSICION_VENTANAS, *DIMENSIONES_VENTANA_JUEGO)
        self.setMinimumSize(*DIMENSIONES_VENTANA_JUEGO)
        self.setWindowTitle(self.titulo_ventana)
        self.iconos = auxiliar.instalar_iconos()
        self.imagenes = auxiliar.instalar_iconos_casillas()
        self.instalar_widgets()

    def dragEnterEvent(self, event) -> None:
        """Permite el Drag and Drop"""
        event.accept()
    
    def dropEvent(self, event) -> None:
        """Analiza donde se soltó el Drag and Drop"""
        posicion = event.pos()
        self.item_seleccionado = event.mimeData().text()
        casilla_seleccionada = auxiliar.obtener_casilla(self.casillas,
                                                        (posicion.x(),
                                                         posicion.y()))
        if not casilla_seleccionada[0]:
            self.alertar("Posición inválida")
        else:
            self.agregar_item(*casilla_seleccionada[1])
        event.accept()

    def mostrar(self) -> None:
        """Muestra la ventana"""
        self.obtener_items()
        self.show()

    def instalar_widgets(self) -> None:
        """Agregar los widgets al layout. Por default es constructor."""
        # Configuración de layouts
        self.layout_principal = QHBoxLayout()
        self.layout_selector = QVBoxLayout()
        self.layout_items = QVBoxLayout()
        self.layout_botones_items = QVBoxLayout()
        self.layout_botones_principales = QHBoxLayout()
        self.layout_boton_salir = QHBoxLayout()

        # Instanciar elementos
        self.selector_categorias = self.instalar_selector()
        self.boton_limpiar = self.instalar_boton_limpiar()
        self.boton_jugar = self.instalar_boton_jugar()
        self.boton_salir = self.instalar_boton_salir()

        # Agregar widgets y stretch
        self.layout_items.addWidget(self.selector_categorias)
        self.layout_selector.addLayout(self.layout_items)
        self.layout_selector.addStretch(1)
        self.layout_selector.addLayout(self.layout_botones_items)
        self.layout_selector.addStretch(7)
        self.layout_botones_principales.addWidget(self.boton_limpiar)
        self.layout_botones_principales.addWidget(self.boton_jugar)
        self.layout_boton_salir.addWidget(self.boton_salir)

        # Agregar y setear layouts
        self.layout_selector.addLayout(self.layout_botones_principales)
        self.layout_selector.addLayout(self.layout_boton_salir)
        self.layout_principal.addLayout(self.layout_selector)
        self.layout_principal.addStretch(6)
        self.instalar_grilla()
        self.setLayout(self.layout_principal)

    def instalar_selector(self) -> None:
        """Instancia el selector de tipos de elementos"""
        selector_tipos = QComboBox(self)
        selector_tipos.addItem('Todos', 0)
        selector_tipos.addItem('Bloques', 1)
        selector_tipos.addItem('Entidades', 2)
        selector_tipos.currentIndexChanged.connect(self.obtener_items)
        return selector_tipos

    def obtener_items(self) -> None:
        """Llama a la señal para mostrar items disponibles"""
        index_selector_tipo = self.selector_categorias.currentIndex()
        self.senal_mostrar_items.emit(index_selector_tipo)

    def instalar_items(self, items: dict) -> None:
        """Instala items visualmente. Es llamado por la señal."""
        # Elimina los botones del Layout
        auxiliar.limpiar_layout(self.layout_botones_items)
        # Instancia nuevos botones y agrega al layout
        for nombre_item in items:
            cantidad = items[nombre_item]
            if nombre_item == "fantasma_followervillain":
                boton_item = BotonMovible(f"ESPECIAL: {cantidad}", self,
                                          nombre_item)
            else:
                boton_item = BotonMovible(f"{cantidad}", self, nombre_item)
            boton_item.setIcon(self.iconos[nombre_item])
            boton_item.setear_pixmap(self.imagenes[nombre_item].scaled(
                *DIMENSION_SPRITES))
            self.layout_botones_items.addWidget(boton_item)

    def instalar_boton_limpiar(self) -> None:
        """Instancia el botón para limpiar el progreso"""
        boton_limpieza = QPushButton("Limpiar", self)
        boton_limpieza.clicked.connect(self.enviar_limpiar_grilla)
        return boton_limpieza

    def instalar_boton_jugar(self) -> None:
        """Instancia el botón para iniciar el juego"""
        boton_jugar = QPushButton("Jugar", self)
        boton_jugar.clicked.connect(self.empezar_juego)
        return boton_jugar

    def instalar_boton_salir(self) -> None:
        """Instancia el botón para salir del juego"""
        boton_salir = QPushButton("Salir", self)
        boton_salir.clicked.connect(self.close)
        return boton_salir

    def instalar_grilla(self) -> None:
        """Instancia elementos de la grilla"""
        self.posiciones_bordes = auxiliar.obtener_posiciones_bordes()
        # Casillas es una lista de listas de la forma [i][j]
        # Lo que permite acceder a la casilla en la posición (i, j)
        self.casillas = [None for i in range(LARGO_GRILLA)]
        for subindice in range(len(self.casillas)):
            self.casillas[subindice] = [None for j in range(ANCHO_GRILLA)]
        # Creación de QLabels (incluye bordes)
        for i in range(LARGO_GRILLA):
            for j in range(ANCHO_GRILLA):
                caja = QLabel("", self)
                caja.setGeometry(230 + j * 32, 25 + i * 32, *DIMENSION_SPRITES)
                if (i, j) in self.posiciones_bordes:
                    caja.setPixmap(self.imagenes["borde"])
                else:
                    auxiliar.estilizar_casilla(caja)
                    caja.setScaledContents(True)
                self.casillas[i][j] = caja

    def agregar_item(self, x: int, y: int) -> None:
        """Envía señal para agregar item en la casilla [i][j]"""
        if self.item_seleccionado is None:
            self.alertar("Selecciona un ítem :c")
        else:
            self.senal_agregar_items.emit(self.item_seleccionado, x, y)
            self.obtener_items()

    def posicionar_item(self, nombre: str, x: int, y: int) -> None:
        """Agrega visualmente item nombre en casilla [i], [j]"""
        self.casillas[x][y].setPixmap(self.imagenes[nombre])

    def enviar_limpiar_grilla(self) -> None:
        """Envía al backend la señal para limpiar la grilla"""
        self.senal_limpiar_grilla.emit()

    def limpiar_grilla(self) -> None:
        """Limpia gráficamente la grilla"""
        for i in range(len(self.casillas)):
            for j in range(len(self.casillas[0])):
                if (i, j) not in self.posiciones_bordes:
                    self.casillas[i][j].setPixmap(QPixmap())
        self.obtener_items()

    def empezar_juego(self) -> None:
        """Emite la señal para empezar el juego"""
        self.senal_intentar_jugar.emit()

    def alertar(self, texto: str) -> None:
        """Levanta una alerta con contenido 'texto'"""
        auxiliar.alertar(texto, "information")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Intenta comenzar el juego presionando enter"""
        if self.juego_iniciado:
            if event.key() == Qt.Key_W:
                self.senal_mover_personaje.emit("w")
            elif event.key() == Qt.Key_A:
                self.senal_mover_personaje.emit("a")
            elif event.key() == Qt.Key_S:
                self.senal_mover_personaje.emit("s")
            elif event.key() == Qt.Key_D:
                self.senal_mover_personaje.emit("d")
        if self.modo_juego == "juego":
            if event.key() == Qt.Key_P:
                self.notificar_pausa()
            if self.juego_iniciado:
                if event.key() == Qt.Key_G:
                    self.senal_solicitar_ganar.emit()

    # Inicializar juego
    def inicializar_juego(self) -> None:
        """Finaliza el modo constructor.
        Inicializa el juego visualmente."""
        self.juego_iniciado = True
        self.modo_juego = "juego"
        self.modo_tiempo = "normal"
        self.boton_limpiar.setEnabled(False)
        self.boton_jugar.setEnabled(False)
        self.limpiar_grilla()
        auxiliar.limpiar_layout(self.layout_botones_items)
        auxiliar.limpiar_layout(self.layout_items)
        self.instalar_labels_juego()
        self.instalar_atajos()

    def instalar_labels_juego(self) -> None:
        """Instancia los QLabels del juego"""
        self.tiempo_label = temporizador.Temporizador(self,
                                                      TIEMPO_CUENTA_REGRESIVA)
        self.tiempo_label.senal_termino_temporizador.connect(
            self.notificar_termino_juego
        )
        self.vidas_label = QLabel('Vidas: [Cargando]', self)
        self.boton_pausar = QPushButton('Pausar', self)
        self.boton_pausar.clicked.connect(self.notificar_pausa)
        self.layout_items.addWidget(self.tiempo_label)
        self.layout_items.addWidget(self.vidas_label)
        self.layout_botones_items.addWidget(self.boton_pausar)

    def actualizar_vidas(self, vidas: int) -> None:
        """Actualiza el texto de la cantidad de vidas"""
        self.vidas_label.setText(f"Vidas: {vidas}")

    def notificar_pausa(self) -> None:
        """Solicita pausar/reanudar el juego al backend"""
        if self.juego_iniciado:
            self.juego_iniciado = False
            self.boton_pausar.setText("Reanudar")
            if self.modo_tiempo == "normal":
                self.tiempo_label.detener_temporizador()
            self.senal_solicitar_pausa.emit(True)
        else:
            self.juego_iniciado = True
            self.boton_pausar.setText("Pausar")
            if self.modo_tiempo == "normal":
                self.tiempo_label.comenzar_temporizador()
            self.senal_solicitar_pausa.emit(False)

    def instalar_elementos_juego(self, elementos: dict) -> None:
        """Instala los elementos en la grilla"""
        self.personajes_instanciados = auxiliar.crear_diccionario_posiciones()
        for personaje in elementos:
            lista_personajes = elementos[personaje]
            for sublista in lista_personajes:
                id_personaje = sublista[0].id
                posiciones = sublista[1]
                personaje_instanciado = self.instanciar_personaje(personaje,
                                                                  posiciones,
                                                                  id_personaje)
                self.personajes_instanciados[personaje].append(
                    personaje_instanciado)
                personaje_instanciado.show()

    def notificar_termino_juego(self) -> None:
        """Notifica al backend del término del juego"""
        self.juego_iniciado = False
        self.senal_fin_tiempo.emit()

    def instanciar_personaje(self, personaje: str, posicion: tuple,
                             id_personaje: int) -> object:
        """Devuelve un personaje instanciado"""
        posicion_casilla = auxiliar.obtener_ubicacion_casilla(self.casillas,
                                                              posicion)
        if personaje == "luigi":
            return Luigi(self, posicion_casilla, id_personaje)
        elif personaje == "fantasma_vertical":
            return objetos.FantasmaVertical(self, posicion_casilla,
                                            id_personaje)
        elif personaje == "fantasma_horizontal":
            return objetos.FantasmaHorizontal(self, posicion_casilla,
                                              id_personaje)
        elif personaje == "fantasma_followervillain":
            return objetos.FantasmaFollowerVillain(self, posicion_casilla,
                                                   id_personaje)
        elif personaje == "pared":
            return objetos.Pared(self, posicion_casilla, id_personaje)
        elif personaje == "roca":
            return objetos.Roca(self, posicion_casilla, id_personaje)
        elif personaje == "fuego":
            return objetos.Fuego(self, posicion_casilla, id_personaje)
        elif personaje == "estrella":
            return objetos.Estrella(self, posicion_casilla, id_personaje)

    def obtener_instancia_personaje(self, lista_personajes: list,
                                    id: int) -> object:
        """Retorna la referencia a la instancia del tipo personaje
        dada una lista de instancias, y su ID de personaje"""
        for nombre_personaje in lista_personajes:
            for posible_personaje in lista_personajes[nombre_personaje]:
                id_personaje = posible_personaje.id
                if id_personaje == id:
                    return posible_personaje

    def aplicar_movimiento(self, id: int, nueva_posicion: tuple) -> None:
        """Mueve el personaje de ID 'id' hacia la nueva posición"""
        lista_personajes = self.personajes_instanciados
        instancia_personaje = self.obtener_instancia_personaje(
            lista_personajes, id)
        posicion_relativa = auxiliar.obtener_ubicacion_casilla(self.casillas,
                                                               nueva_posicion)
        instancia_personaje.movimiento(posicion_relativa)
    
    def ocultar_personaje(self, id: int) -> None:
        """Oculta el personaje id"""
        lista_personajes = self.personajes_instanciados
        instancia_personaje = self.obtener_instancia_personaje(
            lista_personajes, id)
        instancia_personaje.hide()

    def mostrar_personaje(self, id: int) -> None:
        """Muestra el personaje id"""
        lista_personajes = self.personajes_instanciados
        instancia_personaje = self.obtener_instancia_personaje(
            lista_personajes, id)
        instancia_personaje.show()

    def instalar_atajos(self) -> None:
        """Instancia los atajos INF y KIL"""
        self.atajo_kill = QShortcut(QKeySequence("K, I, L"), self)
        self.atajo_inf = QShortcut(QKeySequence("I, N, F"), self)
        self.atajo_kill.activated.connect(self.activar_atajo_kil)
        self.atajo_inf.activated.connect(self.activar_atajo_inf)

    def obtener_tiempo_restante(self) -> None:
        """Envía el tiempo restante al backend"""
        self.senal_enviar_tiempo.emit(self.tiempo_label.tiempo_restante)

    def activar_atajo_kil(self) -> None:
        """Notifica al backend de la
        activación del atajo KIL"""
        if self.juego_iniciado:
            self.senal_matar_fantasmas.emit()

    def activar_atajo_inf(self) -> None:
        """Notifica al backend de la
        activación del atajo INF"""
        if self.juego_iniciado:
            self.tiempo_label.hackear_tiempo()
            self.tiempo_label.setText("TIEMPO HACKEADO")
            self.modo_tiempo = "infinito"
            self.senal_vida_infinita.emit()

    def cerrar_ventana(self) -> None:
        """Cierra la ventana de juego"""
        self.juego_iniciado = False
        self.tiempo_label.detener_temporizador()
        self.hide()

    def reiniciar_partida(self) -> None:
        """Reinicia la partida y abre la ventana"""
        self.juego_iniciado = True
        self.tiempo_label.setText("Tiempo: Cargando...")
        self.modo_juego = "juego"
        self.modo_tiempo = "normal"
        self.tiempo_label.reiniciar_tiempo()
        self.show()
