# Parámetros sobre el torneo
DIAS_TORNEO = 7  # int
ARENA_INICIAL = 'normal'  # 'normal', 'mojada', 'rocosa', 'magnetica'
CANTIDAD_EXCAVADORES_INICIALES = 4  # >0, < excavadores_totales.
METROS_META = 50  # float
POND_ARENA_NORMAL = 0.3  # float entre 0.1 y 1


# Parámetros sobre los ítems.
PROB_ENCONTRAR_ITEM = 0.5
PROB_ENCONTRAR_TESORO = 0.3
PROB_ENCONTRAR_CONSUMIBLE = 0.7

# Parámetros sobre eventos adversos. Probabilidades L/T/D suman 1.
PROB_INICIAR_EVENTO = 0.4
PROB_LLUVIA = 0.4
PROB_TERREMOTO = 0.1
PROB_DERRUMBE = 0.5
METROS_PERDIDOS_DERRUMBE = 5

# Parámetros sobre felicidad, suerte y fuerza
FELICIDAD_PERDIDA = 3
FELICIDAD_ADICIONAL_DOCENCIO = 5
FUERZA_ADICIONAL_DOCENCIO = 5
ENERGIA_PERDIDA_DOCENCIO = 10
ENERGIA_ADICIONAL_TAREO = 10
SUERTE_ADICIONAL_TAREO = 10
EDAD_ADICIONAL_TAREO = 10
FELICIDAD_PERDIDA_TAREO = 2

# Parámetros extra para el funcionamiento de menús
VOLVER = "volver"
SALIR = "salir"

# Paths
CSV_ARENAS = "arenas.csv"
CSV_EXCAVADORES = "excavadores.csv"
CSV_CONSUMIBLES = "consumibles.csv"
CSV_TESOROS = "tesoros.csv"
PARTIDAS = "Partidas"
