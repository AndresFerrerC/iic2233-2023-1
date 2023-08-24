import json
import Scripts.encoding as encoding
import Scripts.cripto as cripto
import pickle


def leer_archivo_json(ruta: str) -> dict:
    """Retorna un diccionario con
    los datos del JSON en la ruta especificada"""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def imprimir_consola(mensaje: str, fondo: str, tipo="SERVIDOR") -> None:
    """Imprime en consola un mensaje con el fondo especificado.
    Opciones: rojo/verde/naranja/azul/morado/cyan/gris"""
    colores = {"rojo": "\033[91m",
               "verde": "\033[92m",
               "naranja": "\033[93m",
               "azul": "\033[94m",
               "morado": "\033[95m",
               "cyan": "\033[96m",
               "gris": "\033[97m"
               }
    print(colores[fondo] + f"[{tipo}] ", end="")
    print(mensaje)


def obtener_objeto_encriptado(objeto: object) -> bytearray:
    """Serializa un objeto y retorna su
    bytearray encriptado y codificado"""
    path_parametros = "parametros.json"
    parametros = leer_archivo_json(path_parametros)
    n_ponderador = parametros["n_ponderador"]
    serializado = encoding.serializar(objeto)
    encriptado = cripto.encriptar(serializado, n_ponderador)
    codificado = encoding.codificar(encriptado)
    return codificado


def desencriptar_objeto(elemento: bytearray) -> object:
    """Decodifica, desencripta el bytearray
    y returna el objeto deserealizado."""
    path_parametros = "parametros.json"
    parametros = leer_archivo_json(path_parametros)
    n_ponderador = parametros["n_ponderador"]
    decodificado = encoding.decodificar(elemento)
    desencriptado = cripto.desencriptar(decodificado, n_ponderador)
    try:
        objeto = pickle.loads(desencriptado)
    except ValueError:
        objeto = False
    except pickle.PickleError:
        objeto = False
    return objeto


def anunciar_inicio_partida() -> None:
    """Anuncia el inicio de una partida"""
    imprimir_consola("Se ha iniciado partida", "verde", "PARTIDA")


def anunciar_jugadores(jugadores: list) -> None:
    """Anuncia los jugadores de la partida"""
    imprimir_consola(f"Jugadores: {' - '.join(jugadores)}", "verde", "PARTIDA")


def anunciar_bot(nombre: str) -> None:
    """Anuncia creación de un bot"""
    imprimir_consola(f"Se ha creado el bot {nombre}", "naranja")


def anunciar_asignacion_nombre(nombre: str) -> None:
    """Anuncia asignación de un nombre"""
    imprimir_consola(f"Se ha asignado el nombre {nombre}", "naranja")


def anunciar_desconexion(nombre: str) -> None:
    """Anuncia la desconexión de un cliente"""
    imprimir_consola(f"Se ha desconectado {nombre}", "rojo", "CLIENTE")


def anunciar_perdida_vida(nombre: str, vidas: int) -> None:
    """Anuncia la pérdida de vida de un jugador"""
    imprimir_consola(f"{nombre} ha perdido una vida. Le quedan {vidas}.",
                     "naranja", "PARTIDA")


def anunciar_muerte(nombre: str) -> None:
    """Anuncia la muerte de un jugador"""
    imprimir_consola(f"Se ha muerto {nombre}", "rojo", "PARTIDA")


def anunciar_turno(nombre: str) -> None:
    """Anuncia el turno de un jugador"""
    imprimir_consola(f"Comienza el turno de {nombre}", "verde", "PARTIDA")


def anunciar_valor(nombre: str, valor: int) -> None:
    """Anuncia el valor de un jugador"""
    imprimir_consola(f"{nombre} ha anunciado el número {valor}", "verde",
                     "PARTIDA")


def anunciar_pasar_turno(nombre: str) -> None:
    """Anuncia el paso de turno de un jugador"""
    imprimir_consola(f"{nombre} ha pasado de turno", "naranja", "PARTIDA")


def anunciar_cambio_dados(nombre: str) -> None:
    """Anuncia el cambio de dados de un jugador"""
    imprimir_consola(f"{nombre} ha cambiado sus dados", "naranja", "PARTIDA")


def anunciar_fin_partida(nombre: str) -> None:
    """Anuncia fin de la partida"""
    imprimir_consola(f"{nombre} ha ganado la partida", "verde", "PARTIDA")
    imprimir_consola("Partida finalizada", "rojo", "PARTIDA")


def anunciar_dudar(nombre: str, nombre_anterior: str,
                   miente: bool) -> None:
    """Anuncia que un jugador ha dudado de otro"""
    if miente:
        imprimir_consola(f"{nombre} ha dudado de {nombre_anterior} (SÍ mentía)",
                         "verde", "PARTIDA")
    else:
        imprimir_consola(f"{nombre} ha dudado de {nombre_anterior}, (NO mentía)",
                         "naranja", "PARTIDA")


def anunciar_poder(nombre: str, poder: str) -> None:
    """Anuncia que se usará un poder"""
    imprimir_consola(f"{nombre} usará el poder {poder}", "verde", "PARTIDA")


def anunciar_poder_aplicado(nombre: str, poder: str, afectado: str) -> None:
    """Anuncia que se usó el poder sobre alguien"""
    imprimir_consola(f"{nombre} usó {poder} sobre {afectado}", "naranja",
                     "PARTIDA")


def anunciar_terremoto(nombre: str, vidas: int) -> None:
    """Anuncia que nombre fue víctima de terremoto"""
    imprimir_consola(f"{nombre} fue víctima de terremoto y quedó con "
                     f" {vidas} vidas", "naranja", "PARTIDA")



def diccionario_info_juego(habilitado: dict,
                           nombre_turno: str,
                           turno_anterior: str,
                           numero_mayor: int,
                           numero_turno: int,
                           nombre_jugadores: dict,
                           jugador_asignado: int,
                           lista_bots: list,
                           dados: dict,
                           vidas: dict) -> dict:
    """Retorna un diccionario con información
    adaptada para ser leída por el cliente"""
    datos = {
        "tipo": "update_juego",
        "habilitado": habilitado,
        "turno": nombre_turno,
        "turno_anterior": turno_anterior,
        "numero_mayor": numero_mayor,
        "numero_turno": numero_turno,
        "jugadores": nombre_jugadores,
        "jugador_asignado": jugador_asignado,
        "lista_bots": lista_bots,
        "dados": dados,
        "vidas": vidas
    }
    return datos


def diccionario_info_inicio(habilitado: bool,
                            jugador_asignado: int,
                            nombre_jugadores: dict) -> dict:
    """Retorna un diccionario con información
    adaptada para ser leída por el cliente"""
    datos = {
        "tipo": "update_inicio",
        "habilitado_jugar": habilitado,
        "jugador_asignado": jugador_asignado,
        "jugadores": nombre_jugadores
    }
    return datos


def diccionario_mensaje(mensaje: str, tipo="warning") -> dict:
    """Retorna un diccionario formateado
    con un mensaje para pop-upear al cliente.
    Tipo warning/information."""
    datos = {
        "tipo": "mensaje",
        "contenido": [mensaje, tipo]
    }
    return datos


def diccionario_abrir_ventana() -> dict:
    """Retorna un diccionario formateado
    para abrir la ventana de juego"""
    datos = {
        "tipo": "abrir_juego"
    }
    return datos


def diccionario_cerrar_juego() -> dict:
    """Retorna un diccionario formateado
    para cerrar la ventana de juego"""
    datos = {
        "tipo": "cerrar_juego"
    }
    return datos


def validar_dado(valor: str, valor_mayor: int) -> bool:
    """Retorna True si el valor anunciado es válido"""
    if not valor.isnumeric():
        return False
    valor_int = int(valor)
    if valor_int < 1 or valor_int > 12:
        return False
    elif valor_int <= valor_mayor:
        return False
    return True

# Auxiliares de la clase Juegos


def obtener_jugadores_disponibles(clientes: dict) -> list:
    """Retorna una lista con los ID disponibles"""
    filtro_usuarios = filter(lambda x: clientes[x] == "Undefined",
                             clientes)
    return list(filtro_usuarios)


def limite_alcanzado(clientes: dict) -> bool:
    """Retorna True si se alcanzó
    límite de jugadores en espera"""
    return len(obtener_jugadores_disponibles(clientes)) == 0


def obtener_nombre_jugadores(lista: bool, clientes: dict,
                             lista_espera: list) -> dict:
    """Retorna dict/lista con los nombres de los jugadores"""
    nombres = {}
    lista_nombres = []
    for cliente in clientes:
        if clientes[cliente] != "Undefined":
            nombres[cliente] = clientes[cliente].nombre
            lista_nombres.append(clientes[cliente].nombre)
        else:
            nombres[cliente] = "Disponible"
    for esperador in lista_espera:
        lista_nombres.append(esperador.nombre)
    if lista:
        return lista_nombres
    else:
        return nombres


def obtener_vida_jugadores(clientes: dict) -> dict:
    """Retorna dict con las vidas de los jugadores"""
    return {i: clientes[i].vidas for i in [x for x in range(1, 5)]}


def obtener_jugadores_vivos(clientes: dict) -> list:
    """Devuelve una lista con los jugadores vivos"""
    filtro_usuarios = filter(lambda x: clientes[x].vidas > 0
                             and not clientes[x].bot,
                             clientes)
    return list(filtro_usuarios)


def obtener_nombre(clientes: dict, lista_espera: list) -> str:
    """Retorna un nombre para ser asignado"""
    path_parametros = "parametros.json"
    parametros = leer_archivo_json(path_parametros)
    posibles_nombres = parametros["nombre_personajes"]
    ocupados = obtener_nombre_jugadores(True, clientes,
                                        lista_espera)
    for nombre in posibles_nombres:
        if nombre not in ocupados:
            return nombre


def obtener_id(clientes: dict, jugador: object) -> int:
    """Retorna índice (int) del dict"""
    for cliente in clientes:
        if clientes[cliente] == jugador:
            return cliente


def obtener_proximo_turno(clientes: dict, actual: int, nueva: bool) -> int:
    """Retorna ID del jugador al que le corresponde después"""
    turno_actual = actual
    if not nueva:
        if turno_actual == 1:
            if clientes[4].vivo:
                return 4
        for i in range(1, 5):
            posible = (turno_actual + i * 3) % 4
            if posible == 0:
                posible = 4
            if clientes[posible].vivo:
                return posible
    else:
        if clientes[turno_actual].vivo:
            return turno_actual
        else:
            return obtener_proximo_turno(clientes, actual, False)


def obtener_id_bots(clientes: dict) -> list:
    """Retorna lista con los IDs de los bots"""
    ids = []
    for cliente in clientes:
        if clientes[cliente] != "Undefined":
            if clientes[cliente].bot:
                ids.append(cliente)
    return ids


def alerta_cola(nombre: str, posicion: int) -> dict:
    """Retorna alerta formateada para enviar"""
    return diccionario_mensaje(f"{nombre}, se ha alcanzado el límite"
                               f"de jugadores. Posición en cola: {posicion}")


def alerta_partida_curso() -> dict:
    """Retorna alerta formateada para enviar"""
    return diccionario_mensaje("Hay una partida en curso.  Intenta más tarde.")


def alerta_partida_iniciada() -> dict:
    """Retorna alerta formateada para enviar"""
    return diccionario_mensaje("Se ha iniciado la partida.  "
                               "Intenta más tarde.")


def alerta_uso_poder(poder: str) -> dict:
    """Retorna alerta formateada para enviar"""
    return diccionario_mensaje(f"¡ {poder} !,  utiliza WASD para seleccionar a"
                               " tu víctima", "information")


def alerta_muerte_dudar() -> dict:
    """Retorna alerta formateada para enviar"""
    return diccionario_mensaje("Quien jugó la última partida murió."
                               "  No puedes dudar.")


def alerta_muerte(nombre: str) -> dict:
    """Retorna alerta formateada para enviar"""
    return diccionario_mensaje(f"{nombre},  has muerto :C.  Puedes"
                               " cerrar el programa.")


def alerta_ganador(nombre: str) -> dict:
    """Retorna alerta formateada para enviar"""
    return diccionario_mensaje(f"{nombre},  ganaste :D.  Puedes"
                               " cerrar el programa.", "information")
