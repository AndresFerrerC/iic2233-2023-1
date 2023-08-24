from PyQt5.QtWidgets import QApplication
import frontend.ventana_inicio as frontend_inicio
import frontend.ventana_juego as ventana_juego
import frontend.ventana_fin as ventana_fin
import backend.backend_inicio as backend_inicio
import backend.backend_constructor as backend_constructor
import backend.backend_juego as backend_juego
import sys


class Aplicacion:
    """Clase que define el flujo de la aplicación"""
    def __init__(self) -> None:
        self.backend_inicio = backend_inicio.Inicio()
        self.ventana_inicial = frontend_inicio.VentanaInicio()
        self.ventana_juego = ventana_juego.VentanaJuego()
        self.ventana_fin = ventana_fin.VentanaFin()
        self.conectar_flujo_principal()

    def conectar_flujo_principal(self) -> None:
        """Conecta el backend y frontend de la primera ventana"""
        self.ventana_inicial.senal_registar_inicio.connect(
            self.backend_inicio.registrar_inicio)
        self.backend_inicio.senal_alertar_inicio.connect(
            self.ventana_inicial.alertar)
        # Abre el juego
        self.backend_inicio.senal_empezar_juego.connect(
            self.ventana_inicial.hide)
        self.backend_inicio.senal_abrir_juego.connect(
            self.iniciar_juego)

    def iniciar_juego(self, nombre: str, mapa: int) -> None:
        """Inicializa el juego o constructor"""
        self.backend_juego = backend_juego.Juego(nombre)
        self.backend_constructor = backend_constructor.Constructor()
        self.conectar_flujo_juego()
        self.ventana_juego.mostrar()
        self.backend_constructor.verificar_carga_mapa(mapa)

    def conectar_flujo_juego(self):
        """Conecta el backend y frontend del juego"""
        self.ventana_juego.senal_mostrar_items.connect(
            self.backend_constructor.mostrar_items)
        self.backend_constructor.senal_instalar_items.connect(
            self.ventana_juego.instalar_items)
        self.ventana_juego.senal_agregar_items.connect(
            self.backend_constructor.agregar_items
        )
        self.backend_constructor.senal_alertar_ventana.connect(
            self.ventana_juego.alertar)
        self.backend_constructor.senal_agregar_item.connect(
            self.ventana_juego.posicionar_item)
        self.ventana_juego.senal_limpiar_grilla.connect(
            self.backend_constructor.limpiar_items
        )
        self.backend_constructor.senal_limpiar_grilla.connect(
            self.ventana_juego.limpiar_grilla)
        
        self.ventana_juego.senal_intentar_jugar.connect(
            self.backend_constructor.registrar_inicio
        )

        # Inicio del juego
        self.backend_constructor.senal_empezar_juego.connect(
            self.backend_juego.iniciar_juego
        )

        self.backend_juego.senal_empezar_juego.connect(
            self.ventana_juego.inicializar_juego
        )
        self.backend_juego.senal_instalar_items_visuales.connect(
            self.ventana_juego.instalar_elementos_juego
        )
        self.backend_juego.senal_mostrar_personaje.connect(
            self.ventana_juego.mostrar_personaje
        )

        # Cheat Codes
        self.ventana_juego.senal_vida_infinita.connect(
            self.backend_juego.vida_infinita
        )
        self.ventana_juego.senal_matar_fantasmas.connect(
            self.backend_juego.matar_todo_fantasma
        )
        # Se acabó el tiempo
        self.ventana_juego.senal_fin_tiempo.connect(
            self.backend_juego.finalizar_tiempo
        )
        # Luigi pide ganar
        self.ventana_juego.senal_solicitar_ganar.connect(
            self.backend_juego.ganar_solicitado
        )
        # Se solicita mover al Luigi
        self.ventana_juego.senal_mover_personaje.connect(
            self.backend_juego.mover_luigi
        )
        # Actualiza las vidas de Luigi
        self.backend_juego.senal_actualizar_vidas.connect(
            self.ventana_juego.actualizar_vidas
        )
        # Se solicita una pausa
        self.ventana_juego.senal_solicitar_pausa.connect(
            self.backend_juego.pausa_solicitada
        )
        # Ocultar personaje del frontend
        self.backend_juego.senal_ocultar_personaje.connect(
            self.ventana_juego.ocultar_personaje
        )
        # Enviar una alerta a la ventana de juego
        self.backend_juego.senal_alertar_ventana.connect(
            self.ventana_juego.alertar)
        # Backend solicita puntaje al frontend (tiempo, etc.)
        self.backend_juego.senal_solicitar_puntaje.connect(
            self.ventana_juego.obtener_tiempo_restante
        )
        # Frontend notifica del tiempo restante al backend
        self.ventana_juego.senal_enviar_tiempo.connect(
            self.backend_juego.establecer_puntaje
        )
        # Movimiento de los personajes
        self.backend_juego.senal_mover_personaje.connect(
            self.ventana_juego.aplicar_movimiento
        )
        # Cierre de la ventana de juego y apertura de término
        self.backend_juego.senal_cerrar_juego.connect(
            self.ventana_juego.cerrar_ventana
        )
        self.backend_juego.senal_abrir_ventana_fin.connect(
            self.ventana_fin.mostrar_ventana
        )

        # Reiniciar y finalizar juego desde la ventana de término
        self.ventana_fin.senal_reiniciar_backend.connect(
            self.backend_juego.reiniciar_partida
        )
        self.ventana_fin.senal_reiniciar_frontend.connect(
            self.ventana_juego.reiniciar_partida
        )

    def iniciar(self) -> None:
        # Muestra la primera ventana
        self.ventana_inicial.show()


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    aplicacion = QApplication([])
    juego = Aplicacion()
    juego.iniciar()
    sys.exit(aplicacion.exec())
