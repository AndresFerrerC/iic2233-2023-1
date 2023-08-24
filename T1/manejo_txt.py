import os
from torneo import Torneo
from parametros import PARTIDAS


def path_destino(archivo: str) -> str:
    """Devuelve un str con el path destino
    en Partidas/archivo.txt."""
    return os.path.join(PARTIDAS, archivo + ".txt")


def opciones_partida() -> list:
    """Retorna una lista con los
    nombres de los archivos disponibles 
    para ser partidas (sin extensiones)."""
    carpeta = os.path.join(PARTIDAS)
    posibles_opciones = os.listdir(carpeta)
    opciones = []
    for i in range(len(posibles_opciones)):
        archivo = os.path.splitext(posibles_opciones[i])
        if archivo[1] == ".txt":
            opciones.append(archivo[0])
    return opciones


def guardar_partida(partida: Torneo, archivo: str) -> str:
    """Guarda la partida en Partidas/archivo.txt.
     Retorna el path relativo donde se ha guardado."""
    path = path_destino(archivo)
    with open(path, "wt", encoding="utf-8") as f:
        # Guardado de ítems
        for item in partida.mochila_items:
            tipo, nombre = item.tipo, item.nombre
            descripcion = item.descripcion
            if tipo == "consumible":
                energia, fuerza = item.energia, item.fuerza
                suerte, felicidad = item.suerte, item.felicidad
                print(f"CONSUMIBLE;{nombre},{descripcion},{energia},{fuerza},"
                      f"{suerte},{felicidad}", file=f)
            elif tipo == "tesoro":
                calidad, cambio = item.calidad, item.cambio
                print(f"TESORO;{nombre},{descripcion},{calidad},{cambio}",
                      file=f)

        # Guardado de excavadores
        for excavador in partida.equipo_excavadores:
            tipo, nombre = excavador.tipo, excavador.nombre
            edad, energia = excavador.edad, excavador.energia
            fuerza, suerte = excavador.fuerza, excavador.suerte
            felicidad = excavador.felicidad
            datos_descanso = excavador.descansando
            descansando, dias_descanso = datos_descanso[0], datos_descanso[1]
            dias_transcurridos_descanso = datos_descanso[2]
            print(f"EXCAVADOR;{tipo},{nombre},{edad},{energia},{fuerza},"
                  f"{suerte},{felicidad},{descansando},{dias_descanso},"
                  f"{dias_transcurridos_descanso}", file=f)

        # Guardado de la arena
        arena = partida.arena_actual
        tipo_arena, nombre_arena = arena.tipo, arena.nombre
        rareza_arena, humedad_arena = arena.rareza, arena.humedad
        dureza_arena, estatica_arena = arena.dureza, arena.estatica
        dificultad_arena = arena.dificultad
        print(f"ARENA;{tipo_arena},{nombre_arena},{rareza_arena},"
              f"{humedad_arena},{dureza_arena},{estatica_arena},"
              f"{dificultad_arena}", file=f)

        # Guardado del Torneo
        meta_torneo, cavado_torneo = partida.meta, partida.metros_cavados
        dias_transcurridos_torneo = partida.dias_transcurridos
        dias_totales_torneo = partida.dias_totales
        print(f"TORNEO;{meta_torneo},{cavado_torneo},"
              f"{dias_transcurridos_torneo},{dias_totales_torneo}", file=f)

    return path
