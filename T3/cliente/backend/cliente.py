from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread
import socket
import auxiliares as auxiliar


class Cliente(QObject):
    senal_actualizar_conectado = pyqtSignal()
    senal_cerrar_ventana = pyqtSignal()
    senal_enviar_alerta = pyqtSignal(list)
    senal_iniciar_ventana_juego = pyqtSignal()
    senal_actualizar_inicio = pyqtSignal(dict)
    senal_actualizar_frontend_juego = pyqtSignal(dict)

    def __init__(self, host: str, puerto: str) -> None:
        """Inicializa el cliente"""
        super().__init__()
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = puerto

    def conectar(self) -> None:
        """Establece la conexión con el servidor"""
        try:
            self.socket_cliente.connect((self.host, self.port))
            thread_escuchar_servidor = Thread(target=self.escuchar_servidor,
                                              args=(self.socket_cliente,),
                                              daemon=True)
            thread_escuchar_servidor.start()
            self.senal_actualizar_conectado.emit()
        except ConnectionError:
            self.cerrar_programa("No se pudo establecer conexión"
                                 " con el servidor.")
            # Ordena el cierre del programa

    def escuchar_servidor(self, socket_servidor: socket.socket) -> None:
        """(Debe llamarse como Thread). Lee al servidor"""
        while True:
            try:
                bytes_largo_datos = socket_servidor.recv(4)
                largo_datos = int.from_bytes(bytes_largo_datos,
                                             byteorder="little")
                respuesta = bytearray()
                respuesta += bytearray(bytes_largo_datos)
                bytes_totales = ((128 + 4) * ((largo_datos // 128))) + 4
                if largo_datos % 128 != 0:
                    bytes_totales += (128 + 4)  # Chunk extra
                if len(bytes_largo_datos) == 0:
                    self.cerrar_programa("Se ha perdido la conexión"
                                         " con el servidor.")
                    break
                # Lectura de los bytes
                while len(respuesta) < bytes_totales:
                    bytes_lectura = min(4096, (bytes_totales) - len(respuesta))
                    respuesta_bytes = socket_servidor.recv(bytes_lectura)
                    respuesta += bytearray(respuesta_bytes)
                # Desencriptación y obtención del objeto
                obj = auxiliar.desencriptar_objeto(respuesta)
                if not obj:
                    self.cerrar_programa("No fue posible desencriptar los "
                                         "datos.  Verificar parametros.json.")
                else:
                    self.interpretar(obj)
            except ConnectionError:
                self.cerrar_programa("Se ha perdido la conexión"
                                     " con el servidor.")
                break

    def desconectar_servidor(self, socket_servidor: socket.socket) -> None:
        """Cierra el socket"""
        socket_servidor.close()

    def interpretar(self, diccionario: dict) -> None:
        """Lee el JSON recibido y lo interpreta"""
        tipo_informacion = diccionario["tipo"]
        if tipo_informacion == "mensaje":
            self.senal_enviar_alerta.emit(diccionario["contenido"])
        elif tipo_informacion == "update_inicio":
            self.senal_actualizar_inicio.emit(diccionario)
        elif tipo_informacion == "abrir_juego":
            self.senal_iniciar_ventana_juego.emit()
        elif tipo_informacion == "update_juego":
            self.senal_actualizar_frontend_juego.emit(diccionario)
        elif tipo_informacion == "cerrar_juego":
            self.cerrar_programa()

    def registrar_inicio(self) -> None:
        """Solicita al servidor iniciar el programa"""
        datos = auxiliar.diccionario_solicitar_jugar()
        self.enviar_informacion(datos)

    def anunciar_valor(self, valor: str) -> None:
        """Notifica al servidor que quiere anunciar valor"""
        datos = auxiliar.diccionario_anunciar_valor(valor)
        self.enviar_informacion(datos)

    def pasar_turno(self) -> None:
        """Notifica al servidor que quiere pasar turno"""
        datos = auxiliar.diccionario_pasar_turno()
        self.enviar_informacion(datos)

    def dudar(self) -> None:
        """Notifica al servidor que se duda"""
        datos = auxiliar.diccionario_dudar()
        self.enviar_informacion(datos)

    def cambiar_dados(self) -> None:
        """Solicita al servidor cambiar dados"""
        datos = auxiliar.diccionario_cambiar_dados()
        self.enviar_informacion(datos)

    def usar_poder(self) -> None:
        """Notifica al servidor el uso de poder"""
        datos = auxiliar.diccionario_usar_poder()
        self.enviar_informacion(datos)

    def aplicar_poder(self, victima: int) -> None:
        """Notifica al servidor de aplicación de poder"""
        datos = auxiliar.diccionario_aplicar_poder(victima)
        self.enviar_informacion(datos)

    def enviar_informacion(self, datos: object) -> None:
        """Envía la información al socket del servidor"""
        try:
            codificado = auxiliar.obtener_objeto_encriptado(datos)
            self.socket_cliente.sendall(codificado)
        except BrokenPipeError:
            self.cerrar_programa("No se pudo establecer conexión"
                                 " con el servidor.")
        except ConnectionError:
            self.cerrar_programa("No se pudo establecer conexión"
                                 " con el servidor.")

    def cerrar_programa(self, mensaje=None) -> None:
        """Cierra el programa.
        Opcionalmente emite un mensaje."""
        if mensaje is not None:
            self.senal_enviar_alerta.emit([mensaje, "warning"])
        self.senal_cerrar_ventana.emit()
