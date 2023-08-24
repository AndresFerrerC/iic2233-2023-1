import auxiliares as auxiliar
import random
import time


class Jugador:
    def __init__(self, socket=None, bot=False) -> None:
        """Instancia un jugador con sus parámetros"""
        # Parámetros
        self.path_parametros = "parametros.json"
        self.parametros = auxiliar.leer_archivo_json(self.path_parametros)
        # Datos
        self.nombre = "Undefined"
        self.socket = socket
        self.see_hack = False
        self.bot = bot
        self.conectado = True
        self.vivo = True
        self.vidas = self.parametros["numero_vidas"]
        self.dados = ["Undefined", "Undefined"]
        self.habilitado = {"turno": False, "dudar": False,
                           "poder": False, "cambiar": False,
                           "dudar_teclas": None}
        self.suma_dados = None

    def cerrar_conexion(self) -> None:
        """Cierra el socket"""
        if self.socket is not None:
            self.socket.close()

    def lanzar_dados(self) -> None:
        """Cambia los dados del jugador"""
        dado_1 = random.randint(1, 6)
        dado_2 = random.randint(1, 6)
        self.suma_dados = dado_1 + dado_2
        self.dados = [dado_1, dado_2]

    def setear_habilitado(self, turno=True, dudar=True, cambiar=True) -> None:
        """Resetea los valores de cada turno"""
        self.habilitado["turno"] = turno
        if turno:
            self.habilitado["dudar"] = dudar
            self.habilitado["cambiar"] = cambiar
            self.revisar_poder()
        else:
            # Nuevo TURNO
            self.poder = None
            self.habilitado = {"turno": False, "dudar": False,
                               "poder": False, "cambiar": False,
                               "dudar_teclas": None}

    def habilitar_poder(self, clientes: dict) -> None:
        """"Habilita el uso de poderes"""
        habilitados = {}
        for cliente in clientes:
            habilitados[cliente] = clientes[cliente].vivo
        self.habilitado["dudar_teclas"] = habilitados
        self.habilitado["turno"] = False  # No puede

    def cambiar_dados(self) -> None:
        """Cambia los dados"""
        if self.habilitado["cambiar"]:
            self.lanzar_dados()
            auxiliar.anunciar_cambio_dados(self.nombre)
            self.habilitado["cambiar"] = False
            self.habilitado["dudar"] = False
            self.revisar_poder()

    def revisar_poder(self) -> None:
        """Revisa si puede utilizar poder"""
        if 1 in self.dados and 2 in self.dados:  # (1, 2)
            self.habilitado["poder"] = True
            self.poder = "Ataque"
        elif 1 in self.dados and 3 in self.dados:
            self.habilitado["poder"] = True
            self.poder = "Terremoto"

    def restar_vidas(self) -> bool:
        """Resta una vida. Retorna True si se murió."""
        self.vidas -= 1
        if self.vidas <= 0:
            return True
        return False

    def terremotear(self) -> None:
        """Aplica terremoto"""
        self.vidas = random.randint(1, self.parametros["numero_vidas"])

    def actuar_bot(self, mayor: int, puede_dudar: bool) -> str:
        """Retorna el actuar del bot"""
        prob_dudar = self.parametros["prob_dudar"]
        prob_anunciar = self.parametros["prob_anunciar"]
        cooldown = self.parametros["cooldown_bots"]
        time.sleep(cooldown)
        if random.random() <= prob_dudar and puede_dudar:
            return ["dudar"]
        else:
            self.cambiar_dados()
            if random.random() <= prob_anunciar:
                numero = random.randint(1, 12)
                if numero != 12 and numero > mayor:
                    return ["anunciar", str(numero)]
        return ["pasar"]
