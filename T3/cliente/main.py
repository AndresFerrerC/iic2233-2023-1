from PyQt5.QtWidgets import QApplication
import auxiliares as auxiliar
import frontend.ventana_inicio as ventana_inicio
import frontend.ventana_juego as ventana_juego
import backend.cliente as backend_cliente
import frontend.alertas as alertas
import sys


class Aplicacion:
    """Clase que define el cliente"""
    path_parametros = "parametros.json"
    parametros = auxiliar.leer_archivo_json(path_parametros)

    def __init__(self, puerto: int) -> None:
        """Crea la conexión e inicializa las ventanas"""
        self.ventana_inicial = ventana_inicio.VentanaInicio()
        self.ventana_juego = ventana_juego.VentanaJuego()
        self.puerto = puerto
        self.backend_cliente = backend_cliente.Cliente(
            self.parametros["host"],
            self.puerto
        )
        self.conectado = False
        self.modo = "inicio"
        self.conectar_flujo()

    def conectar_flujo(self) -> None:
        """Instala las señales entre el frontend y backend"""
        # Conexión
        self.backend_cliente.senal_actualizar_conectado.connect(
            self.actualizar_conectado
        )
        # Pop-ups
        self.backend_cliente.senal_enviar_alerta.connect(self.alertar)
        # Solicitar inicio del juego
        self.ventana_inicial.senal_registar_inicio.connect(
            self.backend_cliente.registrar_inicio)
        self.backend_cliente.senal_iniciar_ventana_juego.connect(
            self.iniciar_juego
        )
        # Cierre de la ventana de juego
        self.backend_cliente.senal_cerrar_ventana.connect(self.cerrar)
        # Actualizar datos del frontend
        self.backend_cliente.senal_actualizar_inicio.connect(
            self.ventana_inicial.actualizar_frontend
        )
        self.backend_cliente.senal_actualizar_frontend_juego.connect(
            self.ventana_juego.actualizar_frontend
        )
        # Botones del juego
        self.ventana_juego.senal_anunciar_valor.connect(
            self.backend_cliente.anunciar_valor
        )
        self.ventana_juego.senal_pasar_turno.connect(
            self.backend_cliente.pasar_turno
        )
        self.ventana_juego.senal_dudar.connect(
            self.backend_cliente.dudar
        )
        self.ventana_juego.senal_cambiar_dados.connect(
            self.backend_cliente.cambiar_dados
        )
        self.ventana_juego.senal_usar_poder.connect(
            self.backend_cliente.usar_poder
        )
        # Aplicación de poder
        self.ventana_juego.senal_aplicar_poder.connect(
            self.backend_cliente.aplicar_poder
        )

    def conectar_servidor(self) -> None:
        """Establece la conexión al servidor"""
        self.backend_cliente.conectar()

    def iniciar(self) -> None:
        """Inicializa el flujo del juego"""
        self.ventana_inicial.show()
        self.conectar_servidor()

    def actualizar_conectado(self) -> None:
        """Setea el parámetro conectado a true"""
        self.conectado = True

    def iniciar_juego(self) -> None:
        """Inicia la ventana del juego"""
        self.ventana_inicial.hide()
        self.ventana_juego.show()
        self.modo = "juego"

    def alertar(self, datos: list) -> None:
        """Envía una alerta. [mensaje, tipo].
        Tipo puede ser information o warning."""
        alertas.notificar(*datos)

    def cerrar(self) -> None:
        """Cierra el programa"""
        if self.modo == "inicio":
            self.ventana_inicial.close()
        else:
            self.ventana_juego.close()
        if not self.conectado:
            sys.exit()


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook
    if len(sys.argv) < 2:
        print("Uso del programa: main.py [PUERTO]")
    elif not sys.argv[1].isnumeric():
        print("Recuerda especificar un puerto.")
    else:
        puerto = int(sys.argv[1])
        aplicacion = QApplication([])
        juego = Aplicacion(puerto)
        juego.iniciar()
        sys.exit(aplicacion.exec())
