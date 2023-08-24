# Grilla del juego
ANCHO_GRILLA = 11 # NO EDITAR
LARGO_GRILLA = 16 # NO EDITAR

# -- Todas las ventanas --
POSICION_VENTANAS = (300, 350)

# -- Ventana de inicio --

DIMENSIONES_VENTANA_INICIO = (420, 476)
TITULO_VENTANA_INICIO = "DCCazaFantasmas - Inicio"
PONDERACION_DIMENSIONES_FONDO = 0.95
PATH_LOGO = [".", "sprites", "Elementos", "logo.png"]
PATH_FONDO = [".", "sprites", "Fondos", "fondo_inicio.png"]

# -- Juego -- 
TIEMPO_CUENTA_REGRESIVA = 30  # segundos
MIN_CARACTERES = 3
MAX_CARACTERES = 8
CANTIDAD_VIDAS = 3
MIN_VELOCIDAD = 1.5  # Fantasmas
MAX_VELOCIDAD = 2  # Fantasmas
INTERVALO_SPRITES = 70  # Animación: duración de 1 sprite en ms
MULTIPLICADOR_PUNTAJE = 4
COOLDOWN_FANTASMAS = 0.5  # Segundos antes de que empiecen a moverse los fantasmas
# -- Ventana de juego --
DIMENSIONES_VENTANA_JUEGO = (600, 600)
TITULO_VENTANA_JUEGO = "DCCazaFantasmas - Juego"

# -- Sprites e íconos --
PATH_BORDER = [".", "sprites", "Elementos", "bordermap.png"]
PATH_SPRITES = [".", "sprites"]
ICONOS_BLOQUES = {"estrella": "osstar",
                  "roca": "rock",
                  "fuego": "fire",
                  "pared": "wall"}
ICONOS_ENTIDADES = {"luigi": "luigi_front",
                    "fantasma_vertical": "red_ghost_vertical_1",
                    "fantasma_horizontal": "white_ghost_rigth_3",
                    "fantasma_followervillain": "red_ghost_vertical_2"}

# -- Constructor y clases --
MAXIMO_LUIGI = 1  # No alterar
MAXIMO_ESTRELLA = 1  # No alterar
MAXIMO_FANTASMAS_VERTICAL = 4
MAXIMO_FANTASMAS_HORIZONTAL = 2
MAXIMO_FANTASMAS_FOLLOWER = 1
MAXIMO_PARED = 5
MAXIMO_ROCA = 3
MAXIMO_FUEGO = 2
# -- Lista y path de personajes disponibles --
LISTA_ENTIDADES = ["luigi", "fantasma_vertical",
                   "fantasma_horizontal", "fantasma_followervillain"]
LISTA_BLOQUES = ["pared", "roca", "fuego", "estrella"]
PATH_BLOQUES = [".", "sprites", "Elementos"]
PATH_PERSONAJES = [".", "sprites", "Personajes"]
MATAN_LUIGI = ["fuego", "fantasma_horizontal",
               "fantasma_vertical",
               "fantasma_followervillain"]  # Si tocan a Luigi, lo matan
CAMBIAN_DIRECCION_FANTASMA = ["roca", "pared", "borde"]
# Luigi
IMAGENES_LUIGI = {"up": [f"luigi_up_{i}.png" for i in range(1, 4)],
                  "down": [f"luigi_down_{i}.png" for i in range(1, 4)],
                  "left": [f"luigi_left_{i}.png" for i in range(1, 4)],
                  "right": [f"luigi_rigth_{i}.png" for i in range(1, 4)],
                  "front": ["luigi_front.png"]}

# Fantasmas
IMAGENES_FANTASMA_VERTICAL = [f"red_ghost_vertical_{i}.png" for i in range(1, 4)]
IMAGENES_FANTASMA_HORIZONTAL = {"left": [f"white_ghost_left_{i}.png" for i in range(1, 4)],
                                "right": [f"white_ghost_rigth_{i}.png" for i in range(1, 4)]}
IMAGENES_FANTASMA_FOLLOWERVILLAIN = ["red_ghost_vertical_2.png",
                                     "white_ghost_rigth_2.png"]

# -- Ventana de fin --
PATH_WIN_MP3 = ["sounds", "stageClear.wav"]
PATH_LOSS_MP3 = ["sounds", "gameOver.wav"]
PATH_MAPAS = ["mapas"]
DIMENSIONES_VENTANA_FIN = (200, 250)
DIMENSION_SPRITES = (32, 32)
