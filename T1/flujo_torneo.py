from __future__ import annotations
from arenas import Arena, ArenaNormal, ArenaRocosa, \
    ArenaMojada, ArenaMagnetica
from excavadores import Excavador, ExcavadorDocencio, \
      ExcavadorHibrido, ExcavadorTareo
from items import Item, Consumibles, Tesoros
from parametros import ARENA_INICIAL, CANTIDAD_EXCAVADORES_INICIALES
import torneo
import lectura_csv as csv


def instanciar_arena(tipo: str, datos=[]) -> Arena:
    """Devuelve la arena instanciada del tipo
    especificado. La variable datos es una
    lista opcional: si se especifica, se hará
    uso de aquellos datos en vez de los que
    son entregados por csv.obtener_arena()."""
    if len(datos) == 0:
        datos_arena = csv.obtener_arena(tipo)
    else:
        datos_arena = datos
    nombre, tipo, rareza = datos_arena[0], datos_arena[1], datos_arena[2]
    humedad, dureza, estatica = datos_arena[3], datos_arena[4], datos_arena[5]
    if tipo == "normal":
        arena = ArenaNormal(nombre, rareza, humedad, dureza, estatica)
    elif tipo == "rocosa":
        arena = ArenaRocosa(nombre, rareza, humedad, dureza, estatica)
    elif tipo == "mojada":
        arena = ArenaMojada(nombre, rareza, humedad, dureza, estatica)
    elif tipo == "magnetica":
        arena = ArenaMagnetica(nombre, rareza, humedad, dureza, estatica)
    return arena


def instanciar_nuevo_excavador(tipo: str, nombre: str, edad: int,
                               energia: int, fuerza: int, suerte: int,
                               felicidad: int) -> Excavador:
    """Devuelve un objeto con excavador instanciado"""
    instancia = None
    if tipo == "docencio":
        instancia = ExcavadorDocencio(nombre, edad, energia, fuerza,
                                      suerte, felicidad)
    elif tipo == "tareo":
        instancia = ExcavadorTareo(nombre, edad, energia, fuerza,
                                   suerte, felicidad)
    elif tipo == "hibrido":
        instancia = ExcavadorHibrido(nombre, edad, energia, fuerza,
                                     suerte, felicidad)
    return instancia


def instanciar_excavadores() -> list:
    """Devuelve lista con excavadores instanciados"""
    lista = csv.obtener_excavadores(CANTIDAD_EXCAVADORES_INICIALES)
    lista_excavadores = []
    for excavador in lista:
        tipo = excavador[1]
        nombre, edad, energia = excavador[0], excavador[2], excavador[3]
        fuerza, suerte, felicidad = excavador[4], excavador[5], excavador[6]
        instancia = instanciar_nuevo_excavador(tipo, nombre, edad, energia,
                                               fuerza, suerte, felicidad)
        lista_excavadores.append(instancia)
    return lista_excavadores


def nuevo_excavador_tipo(tipo: str) -> Excavador:
    """Devuelve un excavador instanciado
    que cumpla con ser del tipo"""
    encontrado = False
    excavador = None
    while not encontrado:
        posible_excavador = csv.obtener_excavadores(1)[0]
        if posible_excavador[1] == tipo:
            excavador = posible_excavador
            encontrado = True
    nombre, edad, energia = excavador[0], excavador[2], excavador[3]
    fuerza, suerte, felicidad = excavador[4], excavador[5], excavador[6]
    return instanciar_nuevo_excavador(tipo, nombre, edad, energia,
                                      fuerza, suerte, felicidad)


def cargar_excavador(datos: list) -> Excavador:
    """Devuelve una instancia de excavador
    al cargar partida. La diferencia es que
    este incluye datos sobre el descanso."""
    instancia = None
    tipo, nombre = datos[0], datos[1]
    edad, energia = int(datos[2]), int(datos[3])
    fuerza, suerte = int(datos[4]), int(datos[5])
    felicidad, descansando = int(datos[6]), datos[7]
    dias_descanso = int(datos[8])
    dias_transcurridos_descanso = int(datos[9])
    if descansando == "True":
        estado_descanso = True
    else:
        estado_descanso = False
    if tipo == "docencio":
        instancia = ExcavadorDocencio(nombre, edad, energia,
                                      fuerza, suerte, felicidad)
    elif tipo == "tareo":
        instancia = ExcavadorTareo(nombre, edad, energia,
                                   fuerza, suerte, felicidad)
    elif tipo == "hibrido":
        instancia = ExcavadorHibrido(nombre, edad, energia,
                                     fuerza, suerte, felicidad)
    instancia.descansando = [estado_descanso, dias_descanso,
                             dias_transcurridos_descanso]

    return instancia


def instanciar_consumible(datos=[]) -> Consumibles:
    """Devuelve un consumible instanciado.
    La variable datos puede corresponder a una lista
    con los datos en el mismo orden de obtener_consumible().
    Por defecto, esta lista está vacía, lo que implica
    que se desea un consumible random."""
    if len(datos) == 0:
        consumible_lista = csv.obtener_consumible()
    else:
        consumible_lista = datos
    nombre, descripcion = consumible_lista[0], consumible_lista[1]
    energia, fuerza = int(consumible_lista[2]), int(consumible_lista[3])
    suerte, felicidad = int(consumible_lista[4]), int(consumible_lista[5])
    return Consumibles(nombre, descripcion, energia, fuerza,
                       suerte, felicidad)


def instanciar_tesoro(datos=[]) -> Tesoros:
    """Devuelve un tesoro instanciado.
    La variable datos puede corresponder a una lista
    con los datos en el mismo orden de obtener_tesoro().
    Por defecto, la lista está vacía, lo que implica
    que se desea un consumible random."""
    if len(datos) == 0:
        tesoro_lista = csv.obtener_tesoro()
    else:
        tesoro_lista = datos
    nombre, descripcion = tesoro_lista[0], tesoro_lista[1]
    calidad, cambio = int(tesoro_lista[2]), tesoro_lista[3]
    return Tesoros(nombre, descripcion, calidad, cambio)


def obtener_items_instanciados() -> Item:
    """Entrega una lista con todos los
    posibles items ya instanciados"""
    items = []
    lista_tesoros = csv.lista_tesoros()
    lista_consumibles = csv.lista_consumibles()
    for tesoro in lista_tesoros:
        tesoro_instanciado = instanciar_tesoro(tesoro)
        items.append(tesoro_instanciado)
    for consumible in lista_consumibles:
        consumible_instanciado = instanciar_consumible(consumible)
        items.append(consumible_instanciado)
    return items


def nueva_partida():
    """Crea una nueva partida con
    los datos iniciales por defecto"""
    partida = torneo.Torneo()
    arena = instanciar_arena(ARENA_INICIAL)
    excavadores = instanciar_excavadores()
    partida.arena_actual = arena
    partida.equipo_excavadores = excavadores
    return partida


def cargar_partida_vacia():
    """Instancia una clase Torneo().
    El torneo está absolutamente vacío,
    sin excavadores ni arena. La función
    tiene como propósito el que se le
    agreguen instancias manualmente
    a esta partida."""
    partida = torneo.Torneo()
    return partida
