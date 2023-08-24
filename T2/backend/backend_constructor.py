from PyQt5.QtCore import QObject, pyqtSignal
from parametros import MAXIMO_ESTRELLA, MAXIMO_FANTASMAS_HORIZONTAL, \
    MAXIMO_FANTASMAS_VERTICAL, MAXIMO_FUEGO, MAXIMO_LUIGI, MAXIMO_PARED, \
    MAXIMO_ROCA, LISTA_ENTIDADES, LISTA_BLOQUES, MAXIMO_FANTASMAS_FOLLOWER
import auxiliares as auxiliar
import os


class Constructor(QObject):
    senal_alertar_ventana = pyqtSignal(str)
    senal_instalar_items = pyqtSignal(dict)
    senal_agregar_item = pyqtSignal(str, int, int)
    senal_limpiar_grilla = pyqtSignal()
    # Señal que inicia el juego
    senal_empezar_juego = pyqtSignal(dict)
    
    def __init__(self) -> None:
        super().__init__()
        self.casillas_ocupadas = []
        self.nombre_bloques = LISTA_BLOQUES
        self.nombre_entidades = LISTA_ENTIDADES
        self.obtener_items_iniciales()
        self.posicion_elementos = auxiliar.crear_diccionario_posiciones()

    def obtener_items_iniciales(self) -> None:
        """Instancia las cantidades iniciales de entidades y bloques"""
        self.entidades = {"luigi": MAXIMO_LUIGI,
                          "fantasma_vertical": MAXIMO_FANTASMAS_VERTICAL,
                          "fantasma_horizontal": MAXIMO_FANTASMAS_HORIZONTAL,
                          "fantasma_followervillain": MAXIMO_FANTASMAS_FOLLOWER}
        self.bloques = {"pared": MAXIMO_PARED,
                        "roca": MAXIMO_ROCA,
                        "fuego": MAXIMO_FUEGO,
                        "estrella": MAXIMO_ESTRELLA}

    def obtener_diccionario_items(self) -> dict:
        """Retorna un diccionario con todos los items
        y sus cantidades disponibles"""
        diccionario_items = self.entidades.copy()
        return diccionario_items.update(self.bloques)

    def mostrar_items(self, tipo: int) -> None:
        """Actualiza el frontend con las cantidades actuales del tipo
        0 = Todos, 1 = Bloques, 2 = Entidades"""
        if tipo == 0:
            diccionario_actual = self.entidades.copy()
            diccionario_actual.update(self.bloques)  # agrega
        elif tipo == 1:
            diccionario_actual = self.bloques
        elif tipo == 2:
            diccionario_actual = self.entidades
        self.senal_instalar_items.emit(diccionario_actual)

    def agregar_items(self, nombre: str, x: int, y: int) -> None:
        """Agrega item 'nombre' en la casilla x,y y actualiza el frontend"""
        posicion = (x, y)
        item = nombre
        # Lista a revisar
        if item in self.nombre_bloques:
            diccionario_de_items = self.bloques
        else:
            diccionario_de_items = self.entidades
        cantidad = diccionario_de_items[item]

        if posicion in self.casillas_ocupadas:
            self.senal_alertar_ventana.emit("La casilla ya está ocupada")
        elif cantidad <= 0:
            self.senal_alertar_ventana.emit("¡No quedan ítems!")
        else:
            self.casillas_ocupadas.append(posicion)
            self.posicion_elementos[item].append(posicion)
            diccionario_de_items[item] -= 1
            self.senal_agregar_item.emit(nombre, x, y)

    def limpiar_items(self) -> None:
        """Limpia la grilla y notifica al frontend"""
        self.casillas_ocupadas = []
        self.posicion_elementos = auxiliar.crear_diccionario_posiciones()
        self.obtener_items_iniciales()
        self.senal_limpiar_grilla.emit()
        self.senal_alertar_ventana.emit("Se ha limpiado la grilla")

    def verificar_carga_mapa(self, mapa: int) -> None:
        """Verifica que exista el mapa a pre-cargar"""
        lista_mapas = auxiliar.obtener_mapas()
        if mapa in lista_mapas:
            path_mapa = os.path.join("mapas", lista_mapas[mapa] + ".txt")
            self.posicion_elementos = self.obtener_elementos_mapa(path_mapa)
            self.entidades["luigi"] = 0  # override
            self.bloques["estrella"] = 0  # override
            self.registrar_inicio()

    def obtener_elementos_mapa(self, mapa: str) -> dict:
        """Retorna un dict con los elementos desde
        la posición relativa de nombre mapa"""
        casillas = []
        with open(mapa, "rt", encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip()
                casillas.append([caracter for caracter in linea])
        diccionario = auxiliar.crear_diccionario_posiciones()
        personajes = {"L": "luigi", "P": "pared", "F": "fuego",
                      "H":  "fantasma_horizontal", "V": "fantasma_vertical",
                      "S": "estrella", "R": "roca"}
        for i in range(len(casillas)):
            for j in range(len(casillas[i])):
                personaje = casillas[i][j]
                if personaje != "-":
                    diccionario[personajes[personaje]].append((i + 1, j + 1))
        return diccionario

    def registrar_inicio(self) -> None:
        """Verifica que se cumplan las condiciones para
        empezar el juego y notifica al backend del juego"""
        if self.entidades["luigi"] != 0:
            self.senal_alertar_ventana.emit("Debe estar Luigi")
        elif self.bloques["estrella"] != 0:
            self.senal_alertar_ventana.emit("Debe haber una estrella")
        else:
            self.senal_empezar_juego.emit(self.posicion_elementos)
