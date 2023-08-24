import socket
import random
import time
import auxiliares as auxiliar
from jugador import Jugador
from collections import deque


class Juego:
    def __init__(self):
        """Instancia el juego"""
        self.path_parametros = "parametros.json"
        self.parametros = auxiliar.leer_archivo_json(self.path_parametros)
        self.clientes = {i: "Undefined" for i in [x for x in range(1, 5)]}
        self.lista_espera = deque()
        self.jugando = False

    def setear_parametros_juego(self, inicio=True) -> None:
        """Establece parámetros iniciales para una partida"""
        self.jugando = True  # Resetear
        self.nombre_turno = "Esperando"
        self.turno_anterior = "Esperando"
        self.numero_mayor = 0
        self.numero_turno = 0
        self.ultima_jugada = {"jugador": None, "tipo": None, "miente": None}
        if inicio:
            self.id_turno_anterior = 0
            self.id_jugador_turno = 0

    def aceptar_jugador(self, jugador: Jugador) -> None:
        """Agrega un jugador a un slot disponible"""
        slot = auxiliar.obtener_jugadores_disponibles(self.clientes)[0]
        self.clientes[slot] = jugador

    def añadir_cliente(self, cliente: socket.socket) -> None:
        """Gestiona la unión de un jugador"""
        jugador = Jugador(cliente)
        jugador.nombre = auxiliar.obtener_nombre(self.clientes,
                                                 self.lista_espera)
        auxiliar.anunciar_asignacion_nombre(jugador.nombre)
        if not self.jugando and not auxiliar.limite_alcanzado(self.clientes):
            self.aceptar_jugador(jugador)
        elif auxiliar.limite_alcanzado(self.clientes):
            self.lista_espera.append(jugador)
            posicion_espera = len(self.lista_espera)
            alerta = auxiliar.alerta_cola(jugador.nombre, posicion_espera)
            self.enviar_informacion(jugador, alerta)
        elif self.jugando:
            alerta = auxiliar.alerta_partida_curso()
            self.enviar_informacion(jugador, alerta)
        self.enviar_status_inicio()
        return jugador

    def enviar_informacion(self, usuario: Jugador, datos: object) -> None:
        """Envía información al socket"""
        if usuario.socket is not None and usuario.vivo:
            try:
                socket_cliente = usuario.socket
                codificado = auxiliar.obtener_objeto_encriptado(datos)
                socket_cliente.sendall(codificado)
            except BrokenPipeError:
                self.desconectar_cliente(usuario)
            except ConnectionError:
                self.desconectar_cliente(usuario)

    def enviar_status_inicio(self) -> None:
        """Envía datos para actualizar ventana de inicio"""
        for cliente in self.clientes:
            if self.clientes[cliente] != "Undefined":
                jugador = self.clientes[cliente]
                status = self.obtener_status_inicio(jugador)
                self.enviar_informacion(jugador, status)
        for esperador in self.lista_espera:
            status = self.obtener_status_inicio(esperador)
            self.enviar_informacion(esperador, status)

    def iniciar_juego(self) -> None:
        """Inicializa el juego"""
        self.rellenar_bots()
        lista_nombres = []
        for cliente in self.clientes:
            if self.clientes[cliente].bot:
                lista_nombres.append(self.clientes[cliente].nombre + " (Bot)")
            else:
                lista_nombres.append(self.clientes[cliente].nombre)
            if self.clientes[cliente].socket is not None:
                self.enviar_informacion(self.clientes[cliente],
                                        auxiliar.diccionario_abrir_ventana())
        for esperador in self.lista_espera:
            alerta = auxiliar.alerta_partida_iniciada()
            self.enviar_informacion(esperador, alerta)
        auxiliar.anunciar_inicio_partida()
        auxiliar.anunciar_jugadores(lista_nombres)
        self.iniciar_ronda(True)

    def rellenar_bots(self) -> None:
        """Rellena con bots en caso de no haber players"""
        for cliente in self.clientes:
            if self.clientes[cliente] == "Undefined":
                bot = Jugador(None, True)
                nombre_asignado = auxiliar.obtener_nombre(self.clientes,
                                                          self.lista_espera)
                bot.nombre = nombre_asignado
                self.clientes[cliente] = bot
                auxiliar.anunciar_bot(bot.nombre)

    def obtener_dados(self, jugador: Jugador) -> dict:
        """Retorna dict con los dados de los jugadores.
        Sólo muestra los dados del jugador, salvo que tenga SEE"""
        see = jugador.see_hack
        if see:
            return {i: self.clientes[i].dados for i in [x for x in range(1, 5)]}
        else:
            dict = {i: ["Undefined", "Undefined"] for i in [x for x in range(1, 5)]}
            for cliente in self.clientes:
                if self.clientes[cliente] == jugador:
                    dict[cliente] = jugador.dados
            return dict

    def obtener_bots_vivos(self) -> list:
        """Retorna una lista con los bots vivos"""
        filtro_usuarios = filter(lambda x: self.clientes[x].vidas > 0
                                 and self.clientes[x].bot,
                                 self.clientes)
        return list(filtro_usuarios)

    def obtener_status_inicio(self, jugador: Jugador) -> dict:
        """Retorna un diccionario con el status del inicio"""
        habilitado_jugar = jugador in self.clientes.values()
        if habilitado_jugar:
            jugador_asignado = auxiliar.obtener_id(self.clientes, jugador)
        else:
            jugador_asignado = "Undefined"
        jugadores = auxiliar.obtener_nombre_jugadores(False, self.clientes,
                                                      self.lista_espera)
        return auxiliar.diccionario_info_inicio(habilitado_jugar,
                                                jugador_asignado, jugadores)

    def obtener_status_juego(self, jugador: Jugador) -> dict:
        """Retorna un diccionario para ser enviado al jugador"""
        if self.jugando:
            nombre_turno = self.nombre_turno
            if nombre_turno != jugador.nombre:
                jugador.setear_habilitado(False)
            dict_habilitado = jugador.habilitado
            turno_anterior = self.turno_anterior
            numero_mayor = self.numero_mayor
            numero_turno = self.numero_turno
            lista_bots = auxiliar.obtener_id_bots(self.clientes)
            jugadores = auxiliar.obtener_nombre_jugadores(False, self.clientes,
                                                          self.lista_espera)
            jugador_asignado = auxiliar.obtener_id(self.clientes, jugador)
            dados = self.obtener_dados(jugador)
            vidas = auxiliar.obtener_vida_jugadores(self.clientes)
            return auxiliar.diccionario_info_juego(
                dict_habilitado, nombre_turno, turno_anterior,
                numero_mayor, numero_turno, jugadores,
                jugador_asignado, lista_bots, dados, vidas)

    def desconectar_cliente(self, jugador: Jugador, cerrar_sock=False) -> None:
        """Gestiona una desconexión"""
        auxiliar.anunciar_desconexion(jugador.nombre)
        for cliente in self.clientes:
            if self.clientes[cliente] == jugador:
                if not self.jugando:
                    self.clientes[cliente] = "Undefined"
                    self.correr_lista()
                else:
                    self.eliminar_jugador(jugador, True)
                    if cerrar_sock:
                        cierre_ventana = auxiliar.diccionario_cerrar_juego()
                        self.enviar_informacion(jugador, cierre_ventana)
                        jugador.cerrar_conexion()

        if jugador in self.lista_espera:
            self.lista_espera.remove(jugador)

    def correr_lista(self) -> None:
        """Corre la lista de espera.
        Siempre se llama después de liberar slot"""
        if len(self.lista_espera) > 0:
            jugador_a_aceptar = self.lista_espera.popleft()
            self.aceptar_jugador(jugador_a_aceptar)
        self.enviar_status_inicio()

    def actualizar_juego(self) -> None:
        """Envía status a cada cliente"""
        if self.jugando:
            for cliente in self.clientes:
                if self.clientes[cliente].vivo:
                    status = self.obtener_status_juego(self.clientes[cliente])
                    self.enviar_informacion(self.clientes[cliente], status)

    def iniciar_ronda(self, inicio=True) -> None:
        """Gestiona el inicio de cada ronda"""
        self.setear_parametros_juego(inicio)
        self.lanzar_dados(False)
        self.cambiar_turno(inicio, True, True)

    def lanzar_dados(self, actualizar=True) -> None:
        """Cambia los dados de cada cliente"""
        for cliente in self.clientes:
            if self.clientes[cliente].vivo:
                self.clientes[cliente].lanzar_dados()
        if actualizar:
            self.actualizar_juego()

    def verificar_fin_partida(self) -> bool:
        """Retorna [True, tipo] si se termina la partida
        donde tipo es True si ganó un jugador"""
        if len(self.obtener_bots_vivos()) == 0 and \
                len(auxiliar.obtener_jugadores_vivos(self.clientes)) == 1:
            return [True, True]
        elif len(self.obtener_bots_vivos()) > 0 and \
                len(auxiliar.obtener_jugadores_vivos(self.clientes)) == 0:
            return [True, False]
        return [False, False]

    def cambiar_turno(self, inicio=False, actualizar=True,
                      nueva_ronda=False) -> None:
        """Cambia de turno. Si es inicio, sortea."""
        if self.jugando:
            if self.verificar_fin_partida()[0]:
                self.ganar_partida(self.verificar_fin_partida()[1])
            else:
                puede_dudar = False
                if inicio:
                    self.id_jugador_turno = random.randint(1, 4)
                else:
                    self.id_turno_anterior = self.id_jugador_turno
                    self.turno_anterior = \
                        self.clientes[self.id_turno_anterior].nombre
                    self.id_jugador_turno = auxiliar.obtener_proximo_turno(
                        self.clientes, self.id_jugador_turno, nueva_ronda)
                if self.ultima_jugada["jugador"] is not None:
                    if self.ultima_jugada["jugador"].vivo:
                        puede_dudar = True
                jugador = self.clientes[self.id_jugador_turno]
                self.nombre_turno = jugador.nombre
                jugador.setear_habilitado(True, puede_dudar)
                auxiliar.anunciar_turno(self.nombre_turno)
                self.numero_turno += 1
                if actualizar:
                    self.actualizar_juego()
                if jugador.bot and jugador.vivo:
                    accion = jugador.actuar_bot(self.numero_mayor, puede_dudar)
                    if accion[0] == "pasar":
                        self.pasar_turno(jugador)
                    elif accion[0] == "dudar":
                        self.dudar(jugador)
                    elif accion[0] == "anunciar":
                        self.anunciar_valor(jugador, accion[1])

    def anunciar_valor(self, jugador: Jugador, valor: str) -> None:
        """Anuncia un valor de dado"""
        valido = auxiliar.validar_dado(valor, self.numero_mayor)
        if valido:
            miente = False
            if int(valor) > jugador.suma_dados:
                miente = True
            self.ultima_jugada = {"jugador": jugador, "tipo": "anunciar",
                                  "miente": miente}
            auxiliar.anunciar_valor(jugador.nombre, int(valor))
            self.numero_mayor = int(valor)
            self.cambiar_turno()
        else:
            alerta = auxiliar.diccionario_mensaje("El valor no es válido.")
            self.enviar_informacion(jugador, alerta)

    def pasar_turno(self, jugador: Jugador) -> None:
        """Pasa de turno"""
        miente = False
        if self.parametros["valor_paso"] != jugador.suma_dados:
            miente = True
        self.ultima_jugada = {"jugador": jugador, "tipo": "pasar",
                              "miente": miente}
        self.cambiar_turno()
        auxiliar.anunciar_pasar_turno(jugador.nombre)

    def cambiar_dados(self, jugador: Jugador) -> None:
        """Cambia los dados de un jugador"""
        jugador.cambiar_dados()
        self.actualizar_juego()
        auxiliar.anunciar_cambio_dados(jugador.nombre)

    def dudar(self, jugador: Jugador) -> None:
        """Duda de la jugada anterior"""
        if self.jugando:
            player_anterior = self.ultima_jugada["jugador"]
            if player_anterior.vivo:
                self.mostrar_dados()
                anterior_miente = self.ultima_jugada["miente"]
                auxiliar.anunciar_dudar(jugador.nombre,
                                        player_anterior.nombre,
                                        anterior_miente)
                if anterior_miente:
                    self.quitar_vida(player_anterior)
                    self.id_jugador_turno = auxiliar.obtener_id(
                        self.clientes, player_anterior)
                else:
                    self.quitar_vida(jugador)
                self.iniciar_ronda(False)
            else:
                alerta = auxiliar.alerta_muerte_dudar()
                self.enviar_informacion(jugador, alerta)

    def mostrar_dados(self) -> None:
        """Muestra los dados de todos por [X] Segundos"""
        segundos = self.parametros["tiempo_ver_dados"]
        self.activar_see_hack()
        self.actualizar_juego()
        time.sleep(segundos)
        self.activar_see_hack(False)
        self.actualizar_juego()

    def activar_see_hack(self, estado=True) -> None:
        """Activa el see hack en los usuarios"""
        for cliente in self.clientes:
            self.clientes[cliente].see_hack = estado

    def usar_poder(self, jugador: Jugador) -> None:
        """Hace uso de un poder"""
        auxiliar.anunciar_poder(jugador.nombre, jugador.poder)
        alerta = auxiliar.alerta_uso_poder(jugador.poder)
        jugador.habilitar_poder(self.clientes)
        self.enviar_informacion(jugador, alerta)
        self.actualizar_juego()

    def aplicar_poder(self, jugador: Jugador, id_victima: int) -> None:
        """Aplica un poder"""
        victima = self.clientes[id_victima]
        auxiliar.anunciar_poder_aplicado(jugador.nombre, jugador.poder,
                                         victima.nombre)
        if jugador.poder == "Ataque":
            self.quitar_vida(victima)
        elif jugador.poder == "Terremoto":
            victima.terremotear()
            auxiliar.anunciar_terremoto(victima.nombre, victima.vidas)
        self.id_jugador_turno = id_victima
        self.iniciar_ronda(False)

    def quitar_vida(self, jugador: Jugador) -> None:
        """Resta una vida a un jugador y verifica su muerte (o no)"""
        muerto = jugador.restar_vidas()
        auxiliar.anunciar_perdida_vida(jugador.nombre, jugador.vidas)
        if muerto:
            self.eliminar_jugador(jugador)

    def eliminar_jugador(self, jugador: Jugador, desconectado=False) -> None:
        """Elimina a un jugador de una partida"""
        nombre = jugador.nombre
        if not desconectado and jugador.socket is not None:  # Avisarle
            alerta = auxiliar.alerta_muerte(nombre)
            self.enviar_informacion(jugador, alerta)
        else:
            auxiliar.anunciar_desconexion(nombre)
        jugador.vivo = False
        jugador.dados = ["Undefined", "Undefined"]
        jugador.vidas = -1
        auxiliar.anunciar_muerte(nombre)
        self.actualizar_juego()
        if self.verificar_fin_partida()[0]:
            self.ganar_partida(self.verificar_fin_partida()[1])
        elif self.clientes[self.id_jugador_turno] == jugador:
            self.cambiar_turno()

    def ganar_partida(self, jugador=True) -> None:
        """Finaliza la partida"""
        self.jugando = False
        if jugador:
            usuario = self.clientes[auxiliar.obtener_jugadores_vivos(
                self.clientes)[0]]
            ganador = usuario.nombre
            alerta = auxiliar.alerta_ganador(ganador)
            self.enviar_informacion(usuario, alerta)
        else:
            ganador = "Nadie"
        auxiliar.anunciar_fin_partida(ganador)
        self.desconectar_jugadores_partida()

    def desconectar_jugadores_partida(self) -> None:
        """Elimina los jugadores en partida"""
        for cliente in self.clientes:
            if not isinstance(self.clientes[cliente], str):
                self.desconectar_cliente(self.clientes[cliente], True)
