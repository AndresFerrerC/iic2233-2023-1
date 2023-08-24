import socket
import sys
import auxiliares as auxiliar
import juego as flujo_juego
from threading import Thread, Lock


def escuchar_cliente(instancia_juego: object, jugador: object, lock: Lock) -> None:
    """Se encarga de recibir los mensajes del cliente e interpretarlos"""
    socket_cliente = jugador.socket
    while True:
        try:
            bytes_largo_datos = socket_cliente.recv(4)
            largo_datos = int.from_bytes(bytes_largo_datos,
                                         byteorder="little")
            respuesta = bytearray()
            respuesta += bytearray(bytes_largo_datos)
            bytes_totales = ((128 + 4) * ((largo_datos // 128))) + 4
            if largo_datos % 128 != 0:
                bytes_totales += (128 + 4)  # Chunk extra
            if len(bytes_largo_datos) == 0:
                # Desconexión.
                instancia_juego.desconectar_cliente(jugador)
                break
            # Lectura de los bytes
            while len(respuesta) < bytes_totales:
                bytes_lectura = min(4096, (bytes_totales) - len(respuesta))
                respuesta_bytes = socket_cliente.recv(bytes_lectura)
                respuesta += bytearray(respuesta_bytes)
            # Desencriptación y obtención del objeto
            with lock:
                mensaje = auxiliar.desencriptar_objeto(respuesta)
                if not mensaje:
                    auxiliar.imprimir_consola("No se pudo desencriptar el"
                                              " objeto.", "rojo")
                else:
                    if jugador.vivo:
                        interpretar(mensaje, instancia_juego, jugador)
                    else:
                        break  # Detener Thread
        except BrokenPipeError:
            instancia_juego.desconectar_cliente(jugador)
            break
        except ConnectionError:
            instancia_juego.desconectar_cliente(jugador)
            break
        except AttributeError:
            # Ya se ha des-asignado el cliente.
            break


def interpretar(diccionario: dict, instancia_juego: object,
                jugador: object) -> None:
    """Lee el JSON recibido y lo interpreta"""

    tipo_informacion = diccionario["tipo"]
    if jugador.vivo:
        if tipo_informacion == "solicitar_jugar":
            instancia_juego.iniciar_juego()
        elif tipo_informacion == "anunciar_valor":
            instancia_juego.anunciar_valor(jugador, diccionario["valor"])
        elif tipo_informacion == "pasar_turno":
            instancia_juego.pasar_turno(jugador)
        elif tipo_informacion == "cambiar_dados":
            instancia_juego.cambiar_dados(jugador)
        elif tipo_informacion == "dudar":
            instancia_juego.dudar(jugador)
        elif tipo_informacion == "usar_poder":
            instancia_juego.usar_poder(jugador)
        elif tipo_informacion == "aplicar_poder":
            instancia_juego.aplicar_poder(jugador, diccionario["valor"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        auxiliar.imprimir_consola("Uso del programa: main.py [PUERTO].",
                                  "rojo", "PROGRAMA")
    elif not sys.argv[1].isnumeric():
        auxiliar.imprimir_consola("Recuerda especificar un puerto numérico.",
                                  "rojo", "PROGRAMA")
    else:
        path_parametros = "parametros.json"
        parametros = auxiliar.leer_archivo_json(path_parametros)
        host = parametros["host"]
        port = int(sys.argv[1])
        lock_escuchar = Lock()
        # Se crea el socket, hacemos bind y listen
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.listen()
            instancia_juego = flujo_juego.Juego()
        except PermissionError:
            auxiliar.imprimir_consola("Intenta con un puerto superior a 1024.",
                                      "rojo", "PROGRAMA")
            sys.exit()
        except OSError:
            auxiliar.imprimir_consola("El puerto ya se encuentra ocupado.",
                                      "rojo", "PROGRAMA")
            sys.exit()
        while True:
            try:
                auxiliar.imprimir_consola(f"Recibiendo conexiones en {port}.",
                                          "verde")
                # Aceptamos a un cliente
                socket_cliente, address = sock.accept()
                instancia_jugador = instancia_juego.añadir_cliente(
                    socket_cliente)
                auxiliar.imprimir_consola(f"Nueva conexión: {address[0]}:"
                                          f"{address[1]}", "verde", "CLIENTE")

                # Creamos un thread encargado de escuchar a ese cliente
                thread = Thread(target=escuchar_cliente,
                                args=(instancia_juego, instancia_jugador,
                                      lock_escuchar, ),
                                daemon=True)
                thread.start()

            except ConnectionError:
                auxiliar.imprimir_consola("Ocurrió un error en la conexión.",
                                          "rojo")
                sys.exit()
            except KeyboardInterrupt:
                auxiliar.imprimir_consola("Finaliza sus operaciones.", "rojo")
                sys.exit()
