from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from parametros import INTERVALO_SPRITES, MULTIPLICADOR_PUNTAJE, \
    CANTIDAD_VIDAS, COOLDOWN_FANTASMAS, MATAN_LUIGI, CAMBIAN_DIRECCION_FANTASMA
import auxiliares as auxiliar


class Juego(QObject):
    senal_empezar_juego = pyqtSignal()
    senal_instalar_items_visuales = pyqtSignal(dict)
    senal_mover_personaje = pyqtSignal(int, tuple)
    senal_actualizar_vidas = pyqtSignal(int)
    senal_ocultar_personaje = pyqtSignal(int)
    senal_alertar_ventana = pyqtSignal(str)
    senal_mostrar_personaje = pyqtSignal(int)
    senal_cerrar_juego = pyqtSignal()
    senal_abrir_ventana_fin = pyqtSignal(dict)
    senal_solicitar_puntaje = pyqtSignal()

    def __init__(self, nombre: str) -> None:
        super().__init__()
        self.nombre_jugador = nombre
        self.posiciones_iniciales = None
        self.posiciones_actuales = None
        self.juego_iniciado = False
        self.posiciones_bordes = auxiliar.obtener_posiciones_bordes()
        self.personajes_instanciados = auxiliar.crear_diccionario_posiciones()

    def iniciar_juego(self, elementos: dict) -> None:
        """Instancia los elementos principales del juego"""
        self.habilitado = False  # Para ganar
        self.puntaje = None
        self.tiempo_infinito = False
        self.juego_iniciado = True
        self.posiciones_iniciales = elementos.copy()
        self.posiciones_actuales = auxiliar.crear_diccionario_posiciones()
        self.iniciar_timers_luigi()
        self.iniciar_timer_cooldown_fantasmas()
        self.senal_empezar_juego.emit()
        self.instanciar_lista_personajes()
        self.iniciar_movimiento_fantasmas_tardio()

    def instanciar_lista_personajes(self) -> None:
        """Crea instancias de los personajes fantasmas y luigi"""
        id = 0  # Identificador del personaje
        for personaje in self.posiciones_iniciales:
            lista_posiciones = self.posiciones_iniciales[personaje]
            for posiciones in lista_posiciones:
                personaje_instanciado = auxiliar.instanciar_personaje_backend(
                    personaje, posiciones, id)
                if personaje == "luigi":
                    self.luigi = personaje_instanciado
                    self.senal_actualizar_vidas.emit(
                        personaje_instanciado.vidas)
                elif personaje.startswith("fantasma"):
                    personaje_instanciado.senal_mover.connect(
                        self.mover_fantasma
                    )

                self.posiciones_actuales[personaje].append(
                    [personaje_instanciado, posiciones])
                self.personajes_instanciados[personaje].append(
                    [personaje_instanciado])
                id += 1
        self.posiciones_iniciales = self.posiciones_actuales
        self.senal_instalar_items_visuales.emit(self.posiciones_actuales)

    def actualizar_diccionario_posiciones(self) -> None:
        """Actualiza el diccionario de posiciones actuales"""
        diccionario_vacio = auxiliar.crear_diccionario_posiciones()
        for nombre in self.posiciones_actuales:
            for sublista in self.posiciones_actuales[nombre]:
                referencia = sublista[0]
                posicion = referencia.posicion
                diccionario_vacio[nombre].append([referencia, posicion])
        self.posiciones_actuales = diccionario_vacio

    def iniciar_timers_luigi(self) -> None:
        """Instancia timers que permiten evitar que se
        presionen teclas WASD de forma simultánea"""
        self.moviendo_luigi = False
        self.timer_movimiento_luigi = QTimer()
        self.timer_movimiento_luigi.setInterval(3 * INTERVALO_SPRITES)
        self.timer_movimiento_luigi.timeout.connect(self.cambiar_estado_luigi)

    def iniciar_timer_cooldown_fantasmas(self) -> None:
        """Crea el timer del cooldown de los fantasmas"""
        self.timer_cooldown_fantasmas = QTimer()
        self.timer_cooldown_fantasmas.setInterval(int(COOLDOWN_FANTASMAS * 1000))
        self.timer_cooldown_fantasmas.timeout.connect(
            self.iniciar_movimiento_fantasmas_tardio)
        self.timer_cooldown_fantasmas.start()

    def obtener_posiciones_bloqueadas(self, personaje: str,
                                      posicion_actual: tuple) -> set:
        """Retorna un set con posiciones bloqueadas para 
        el movimiento. Esto depende del tipo de personaje."""
        posiciones_bloqueadas = []
        elementos_bloqueados = []
        if personaje == "luigi":
            elementos_bloqueados = ["pared"]
        elif personaje.startswith("fantasma"):
            elementos_bloqueados = ["pared", "roca"]
        bordes = auxiliar.obtener_posiciones_bordes()
        for personaje_disponible in self.posiciones_actuales:
            if personaje_disponible in elementos_bloqueados:
                personajes = self.posiciones_actuales[personaje_disponible]
                if personajes != []:
                    for sublista in personajes:
                        posicion = sublista[1]
                        if personaje_disponible.startswith("fantasma"):
                            if sublista[0].vivo:
                                if posicion_actual != posicion:
                                    posiciones_bloqueadas.append(posicion)
                        else:
                            if posicion_actual != posicion:
                                posiciones_bloqueadas.append(posicion)

        return set(posiciones_bloqueadas).union(bordes)

    def obtener_instancia_personaje(self, nombre: str,
                                    posicion: tuple) -> object:
        """Retorna la referencia a la instancia del tipo personaje
        dado el nombre del personaje y la posición en la grilla"""
        for sublista in self.personajes_instanciados[nombre]:
            instancia_personaje = sublista[0]
            posicion_casilla = instancia_personaje.posicion
            if posicion == posicion_casilla:
                return instancia_personaje

    def encontrar_elemento(self, posicion: tuple) -> str:
        """Retorna el nombre del tipo de elemento ubicado en
        la posición"""
        for nombre in self.personajes_instanciados:
            for lista_elementos in self.personajes_instanciados[nombre]:
                for posible_personaje in lista_elementos:
                    if posible_personaje.posicion == posicion:
                        return posible_personaje.nombre
        if posicion in self.posiciones_bordes:
            return "borde"
        return None

    def verificar_colisiones(self, posicion: tuple) -> dict:
        """Retorna un diccionario con las
        colisiones en las múltiples direcciones del mapa"""
        colisiones = dict()
        posicion_i, posicion_j = posicion[0], posicion[1]
        colisiones['w'] = self.encontrar_elemento((posicion_i - 1, posicion_j))
        colisiones['a'] = self.encontrar_elemento((posicion_i, posicion_j - 1))
        colisiones['s'] = self.encontrar_elemento((posicion_i + 1, posicion_j))
        colisiones['d'] = self.encontrar_elemento((posicion_i, posicion_j + 1))
        return colisiones

    def obtener_instancia_por_id(self, id: int) -> object:
        """Retorna la instancia dada el id del personaje"""
        for nombre in self.personajes_instanciados:
            for sublista in self.personajes_instanciados[nombre]:
                instancia_personaje = sublista[0]
                id_personaje = instancia_personaje.id
                if id_personaje == id:
                    return instancia_personaje

    def iniciar_movimiento_fantasmas(self) -> None:
        """Inicializa timers de los fantasmas"""
        for nombre in self.personajes_instanciados:
            if nombre.startswith('fantasma'):
                for lista_elementos in self.personajes_instanciados[nombre]:
                    for fantasma in lista_elementos:
                        fantasma.iniciar_movimiento()
    
    def iniciar_movimiento_fantasmas_tardio(self) -> None:
        """Inicializa el movimiento de los fantasmas
        y detiene el timer asociado al cooldown"""
        self.iniciar_movimiento_fantasmas()
        self.timer_cooldown_fantasmas.stop()

    def detener_movimiento_fantasmas(self) -> None:
        """Detiene timers de los fantasmas"""
        for nombre in self.personajes_instanciados:
            if nombre.startswith('fantasma'):
                for lista_elementos in self.personajes_instanciados[nombre]:
                    for fantasma in lista_elementos:
                        fantasma.detener_movimiento()

    def mover_fantasma(self, id: int) -> None:
        """Ejecuta el movimiento del fantasma ID"""
        movimiento_permitido = True
        instancia_fantasma = self.obtener_instancia_por_id(id)
        posicion_fantasma = instancia_fantasma.posicion
        posiciones_bloqueadas = self.obtener_posiciones_bloqueadas(
            'fantasma', posicion_fantasma)
        if instancia_fantasma.nombre == "fantasma_followervillain":
            instancia_fantasma.definir_direccion(self.luigi.posicion,
                                                 posiciones_bloqueadas)
        tipo_movimiento = instancia_fantasma.direccion_movimiento
        if instancia_fantasma.vivo:
            posibles_colisiones = self.verificar_colisiones(
                posicion_fantasma)
            colision = posibles_colisiones[tipo_movimiento]
            nueva_posicion = auxiliar.obtener_nueva_posicion(tipo_movimiento,
                                                             posicion_fantasma)
            if colision in CAMBIAN_DIRECCION_FANTASMA:
                instancia_fantasma.cambiar_direccion()
                tipo_movimiento = instancia_fantasma.direccion_movimiento
                colision = posibles_colisiones[tipo_movimiento]
                nueva_posicion = auxiliar.obtener_nueva_posicion(
                    tipo_movimiento, posicion_fantasma)
            elif colision == "fuego":
                self.matar_fantasma(instancia_fantasma)
            elif colision == "estrella":
                posicion_luigi = self.luigi.posicion
                if posicion_luigi == nueva_posicion:
                    self.quitar_vida_luigi()
                    movimiento_permitido = False
            elif colision == "luigi":
                self.quitar_vida_luigi()
                movimiento_permitido = False
                # Asegurar de que no sea P - F - P
            if colision not in CAMBIAN_DIRECCION_FANTASMA:
                if movimiento_permitido:
                    if nueva_posicion not in posiciones_bloqueadas:
                        self.senal_mover_personaje.emit(id, nueva_posicion)
                        instancia_fantasma.actualizar_posicion(nueva_posicion)
                        self.actualizar_diccionario_posiciones()

    def matar_fantasma(self, fantasma: object) -> None:
        """Mata a un fantasma y lo elimina del mapa"""
        id_fantasma = fantasma.id
        fantasma.vivo = False
        self.senal_ocultar_personaje.emit(id_fantasma)

    def mover_luigi(self, tipo_movimiento: str) -> None:
        """Mueve a Luigi según el tipo de movimiento W-A-S-D"""
        informacion_luigi = self.posiciones_actuales['luigi'][0]
        luigi_backend = informacion_luigi[0]
        id_luigi = luigi_backend.id
        luigi_ubicacion = informacion_luigi[1]
        movimiento_permitido = True
        nueva_posicion = auxiliar.obtener_nueva_posicion(tipo_movimiento,
                                                         luigi_ubicacion)
        posiciones_bloqueadas = self.obtener_posiciones_bloqueadas(
            'luigi', luigi_ubicacion)
        if not self.moviendo_luigi:   
            if nueva_posicion not in posiciones_bloqueadas:
                posibles_colisiones = self.verificar_colisiones(
                    luigi_ubicacion)
                colision = posibles_colisiones[tipo_movimiento]
                if colision == "roca":
                    movimiento_roca = self.mover_roca(nueva_posicion,
                                                      tipo_movimiento)
                    if not movimiento_roca:
                        movimiento_permitido = False
                elif colision == "estrella":
                    self.habilitado = True
                elif colision in MATAN_LUIGI:
                    self.quitar_vida_luigi()
                    movimiento_permitido = False
                if movimiento_permitido:
                    if colision != "estrella":
                        self.habilitado = False
                    self.senal_mover_personaje.emit(id_luigi, nueva_posicion)
                    luigi_backend.actualizar_posicion(nueva_posicion)
                    self.actualizar_diccionario_posiciones()
                    self.moviendo_luigi = True
                    self.timer_movimiento_luigi.start()

    def mover_roca(self, posicion: tuple, tipo_movimiento: str) -> bool:
        """Mueve a la roca en la posición, dado el tipo de movimiento.
        Retorna True si se movió, False si no es posible."""
        roca = self.obtener_instancia_personaje("roca", posicion)
        nueva_posicion = auxiliar.obtener_nueva_posicion(tipo_movimiento,
                                                         posicion)
        posibles_colisiones = self.verificar_colisiones(posicion)
        colision = posibles_colisiones[tipo_movimiento]
        if colision is None:
            self.senal_mover_personaje.emit(roca.id, nueva_posicion)
            roca.actualizar_posicion(nueva_posicion)
            self.actualizar_diccionario_posiciones()
            return True
        return False

    def cambiar_estado_luigi(self) -> None:
        """Cambia el estado de movimiento de Luigi a False"""
        self.moviendo_luigi = False
        self.timer_movimiento_luigi.stop()

    def quitar_vida_luigi(self) -> None:
        """Quita una vida a Luigi y reinicia el mapa"""
        if not self.tiempo_infinito:
            self.luigi.vidas -= 1
        if self.luigi.vidas <= 0:
            self.luigi.vidas = 0
            self.terminar_partida("vida")
        else:
            self.resetear_nivel()
        self.senal_actualizar_vidas.emit(self.luigi.vidas)

    def resetear_nivel(self) -> None:
        """Reinicia el mapa reposicionando elementos y
        reviviendo a los fantasmas que estaban muertos"""
        for nombre in self.posiciones_iniciales:
            for sublista in self.posiciones_iniciales[nombre]:
                referencia = sublista[0]
                posicion_original = sublista[1]
                referencia.actualizar_posicion(posicion_original)
                if referencia.nombre.startswith("fantasma"):
                    referencia.direccion_movimiento = referencia.direccion_inicio
                    if not referencia.vivo:
                        referencia.vivo = True
                        self.mostrar_personaje(referencia.id)
                if referencia.nombre not in ["estrella", "pared", "fuego"]:
                    self.senal_mover_personaje.emit(referencia.id,
                                                    posicion_original)
        self.posiciones_actuales = self.posiciones_iniciales

    def mostrar_personaje(self, id: int) -> None:
        """Le dice al frontend que muestre al personaje id"""
        self.senal_mostrar_personaje.emit(id)

    def pausa_solicitada(self, juego_iniciado: bool) -> None:
        """Pausa el juego si está iniciado el juego. Sino, reanuda."""
        if juego_iniciado:
            self.detener_movimiento_fantasmas()
            self.juego_iniciado = False
        else:
            self.iniciar_movimiento_fantasmas()
            self.juego_iniciado = True

    def ganar_solicitado(self) -> None:
        """Revisa si Luigi puede ganar una vez
        se presiona G. Llamado desde frontend"""
        if self.habilitado:
            self.terminar_partida('luigi')

    def finalizar_tiempo(self) -> None:
        """Recibe la notificación de término
        de tiempo desde el temporizador"""
        self.terminar_partida('tiempo')

    def solicitar_puntaje(self) -> None:
        """Solicita el puntaje restante de la partida"""
        self.senal_solicitar_puntaje.emit()

    def establecer_puntaje(self, tiempo: int) -> None:
        """Establece el puntaje de la partida"""
        self.tiempo_restante = tiempo
        vidas_ocupadas = CANTIDAD_VIDAS - self.luigi.vidas
        if vidas_ocupadas == 0:
            vidas_ocupadas = 1
        self.puntaje = round((tiempo * MULTIPLICADOR_PUNTAJE) / vidas_ocupadas,
                             1)

    def terminar_partida(self, razon: str) -> None:
        """Finaliza la partida y notifica al frontend"""
        self.solicitar_puntaje()
        nombre = self.nombre_jugador
        datos = {}
        datos["estado"] = "LOSS"
        if razon == "tiempo":
            datos["texto_estado"] = f"¡ Se acabó el tiempo,  {nombre} !"
        elif razon == "vida":
            datos["texto_estado"] = f"¡ Te quedaste sin vidas,  {nombre} !"
        else:  # Luigi gana
            datos["estado"] = "WIN"
            datos["texto_estado"] = f"¡ Ganaste,  {nombre} !"
        datos["texto_vidas"] = f"Vidas: {self.luigi.vidas}" \
                               f" - Tiempo restante: {self.tiempo_restante}"
        datos["texto_puntaje"] = f"Puntaje: {self.puntaje}"
        self.senal_cerrar_juego.emit()
        self.senal_abrir_ventana_fin.emit(datos)
        self.detener_movimiento_fantasmas()
        self.juego_iniciado = False

    def vida_infinita(self) -> None:
        """Establece vida infinita y tiempo infinito"""
        self.tiempo_infinito = True
        self.luigi.vidas = CANTIDAD_VIDAS
        self.senal_actualizar_vidas.emit(self.luigi.vidas)

    def matar_todo_fantasma(self) -> None:
        """Mata a todos los fantasmas de la partida"""
        for nombre in self.personajes_instanciados:
            if nombre.startswith('fantasma'):
                for lista_elementos in self.personajes_instanciados[nombre]:
                    for fantasma in lista_elementos:
                        self.matar_fantasma(fantasma)

    def reiniciar_partida(self) -> None:
        """Reinicia la partida"""
        self.resetear_nivel()
        self.luigi.vidas = CANTIDAD_VIDAS
        self.juego_iniciado = True
        self.tiempo_infinito = False
        self.timer_cooldown_fantasmas.start()
        self.senal_actualizar_vidas.emit(self.luigi.vidas)
