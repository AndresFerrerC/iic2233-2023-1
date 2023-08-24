import json
import Scripts.encoding as encoding
import Scripts.cripto as cripto
import pickle


def leer_archivo_json(ruta: str) -> dict:
    """Retorna un diccionario con
    los datos del JSON en la ruta especificada"""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


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


def diccionario_solicitar_jugar() -> dict:
    """Retorna diccionario formateado
    para solicitar jugar al backend"""
    datos = {
        "tipo": "solicitar_jugar"
    }
    return datos


def diccionario_anunciar_valor(valor: str) -> dict:
    """Retorna un diccionario formateado
    para anunciarle valor al backend"""
    datos = {
        "tipo": "anunciar_valor",
        "valor": valor
    }
    return datos


def diccionario_pasar_turno() -> dict:
    """Retorna un diccionario formateado
    para pasarle turno al backend"""
    datos = {
        "tipo": "pasar_turno"
    }
    return datos


def diccionario_cambiar_dados() -> dict:
    """Retorna un diccionario formateado
    para cambiar dados al backend"""
    datos = {
        "tipo": "cambiar_dados"
    }
    return datos


def diccionario_dudar() -> dict:
    """Retorna un diccionario formateado
    para dudar al backend"""
    datos = {
        "tipo": "dudar"
    }
    return datos


def diccionario_usar_poder() -> dict:
    """Retorna un diccionario formateado
    para usar poder al backend"""
    datos = {
        "tipo": "usar_poder"
    }
    return datos


def diccionario_aplicar_poder(victima: int) -> dict:
    """Retorna un diccionario formateado
    para usar poder al backend"""
    datos = {
        "tipo": "aplicar_poder",
        "valor": victima
    }
    return datos
