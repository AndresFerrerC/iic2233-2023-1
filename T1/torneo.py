from __future__ import annotations
from random import randint, choices, choice, random
from items import Consumibles, Tesoros
from parametros import METROS_META, DIAS_TORNEO, PROB_LLUVIA, PROB_TERREMOTO, \
    PROB_DERRUMBE, METROS_PERDIDOS_DERRUMBE, FELICIDAD_PERDIDA, \
    PROB_INICIAR_EVENTO, POND_ARENA_NORMAL
import menu_utils as menu
import flujo_torneo


class Torneo:
    def __init__(self) -> None:
        self.arena_actual = None
        self.equipo_excavadores = []
        self.mochila_items = []
        self.eventos = ["lluvia", "terremoto", "derrumbe"]
        self.metros_cavados = 0
        self.meta = METROS_META
        self.dias_transcurridos = 1
        self.dias_totales = DIAS_TORNEO

    def simular_dia(self) -> None:
        total_cavado = 0
        total_consumibles = 0
        total_tesoros = 0

        if self.arena_actual.tipo == "magnetica":
            self.arena_actual.dureza = randint(1, 10)
            self.arena_actual.humedad = randint(1, 10)
        elif self.arena_actual.tipo == "normal":
            self.arena_actual.dificultad = self.arena_actual.dificultad * \
                POND_ARENA_NORMAL

        print("-" * 80 + "\n" + f"Día {self.dias_transcurridos}".center(75)
              + "\n" + "-" * 80)
        for excavador in self.equipo_excavadores:
            if not excavador.descansando[0]:
                total_cavado += excavador.cavar(self.arena_actual.dificultad)
            else:
                print(f"* [{excavador.nombre}] no puede excavar"
                      " porque está descansando.")
        total_cavado = round(total_cavado, 2)
        self.metros_cavados += total_cavado
        print(f"El equipo ha conseguido excavar {total_cavado} metros.")
        print("\nItems encontrados: ")
        for excavador in self.equipo_excavadores:
            if not excavador.descansando[0]:
                item = excavador.encontrar_item(self.arena_actual.tipo)
                if item == "tesoro":
                    posibles = [item for item in self.arena_actual.items if
                                item.tipo == "tesoro"]
                    encontrado = choice(posibles)
                    self.mochila_items.append(encontrado)
                    print(f"{excavador.nombre} consiguió {encontrado.nombre}"
                          f" del tipo {encontrado.tipo}")
                    total_tesoros += 1
                elif item == "consumible":
                    posibles = [item for item in self.arena_actual.items if
                                item.tipo == "consumible"]
                    encontrado = choice(posibles)
                    self.mochila_items.append(encontrado)
                    print(f"{excavador.nombre} consiguió {encontrado.nombre}"
                          f" del tipo {encontrado.tipo}")
                    total_consumibles += 1
                else:
                    print(f"{excavador.nombre} no consiguió nada.")
            else:
                print(f"* [{excavador.nombre}] no puede encontrar ítems"
                      " porque está descansando.")

        print(f"Se han encontrado {total_consumibles + total_tesoros} ítems:")
        print(f"- {total_consumibles} consumibles.")
        print(f"- {total_tesoros} tesoros.")

        if random() <= PROB_INICIAR_EVENTO:
            self.iniciar_evento()

        for excavador in self.equipo_excavadores:
            # Descuento de energía a quienes no están descansando
            if not excavador.descansando[0]:
                excavador.gastar_energia()

            # Revisión del estado de energía
            if excavador.energia == 0 and not excavador.descansando[0]:
                print(f"*** [{excavador.nombre}] Se me acabó la energía. :c")
                excavador.descansar()
            elif excavador.descansando[0]:
                excavador.descansando[2] += 1
                if excavador.descansando[2] == excavador.descansando[1]:
                    excavador.descansando = [False, 0, 0]
                    excavador.energia = 100
                    print(f"* {excavador.nombre} Está terminando de "
                          "descansar y volverá a excavar mañana c:")
                else:
                    print(f"* [{excavador.nombre} - AFK] Descanso por hoy...")

        self.dias_transcurridos += 1
        if self.dias_transcurridos > self.dias_totales:  # fin
            print("****" * 20)
            print("¡SE HA TERMINADO LA COMPETENCIA!")
            print("****" * 20)
            print(f"* -> Metros excavados: {round(self.metros_cavados, 2)}")
            print(f"* -> Metros de la meta: {self.meta}")
            if self.metros_cavados >= self.meta:
                print("! -> ¡¡GANASTE :D!!")
            else:
                print("! -> Perdiste :c")
            return "ir_menu_inicio"
        return "ir_menu_principal"

    def mostrar_estado(self) -> None:
        menu.imprimir_estado_torneo(self.dias_transcurridos,
                                    self.arena_actual.tipo,
                                    self.arena_actual.nombre,
                                    self.arena_actual.dificultad,
                                    round(self.metros_cavados, 2),
                                    self.meta, self.equipo_excavadores)

    def ver_mochila(self) -> list:
        """Retorna una lista con los elementos en
        la mochila de items."""
        return self.mochila_items

    def usar_consumible(self, consumible: Consumibles) -> None:
        """Llama a cada excavador a consumir."""
        for excavador in self.equipo_excavadores:
            excavador.consumir(consumible)

    def abrir_tesoro(self, tesoro: Tesoros) -> None:
        """Abre un tesoro. Depende de la calidad."""
        cambio = tesoro.cambio
        calidad = tesoro.calidad
        if calidad == 1:
            tipo_excavador = cambio
            nuevo_miembro = flujo_torneo.nuevo_excavador_tipo(tipo_excavador)
            self.equipo_excavadores.append(nuevo_miembro)
        else:  # segunda calidad
            tipo_arena = cambio
            self.arena_actual = flujo_torneo.instanciar_arena(tipo_arena)

    def iniciar_evento(self) -> None:
        """Se inicia un evento. Esta función se llama
        cuando se cumple la probabilidad de iniciar un evento."""
        pesos = [PROB_LLUVIA, PROB_TERREMOTO, PROB_DERRUMBE]
        evento_iniciado = choices(self.eventos, weights=pesos, k=1)
        evento_final = evento_iniciado[0]
        tipo_actual_arena = self.arena_actual.tipo
        print(f"\n¡¡Durante el día de trabajo ocurrió un(a) {evento_final}!!")

        if evento_final == "lluvia":
            if tipo_actual_arena == "normal":
                self.arena_actual = flujo_torneo.instanciar_arena("mojada")
            elif tipo_actual_arena == "rocosa":
                self.arena_actual = flujo_torneo.instanciar_arena("magnetica")
        elif evento_final == "terremoto":
            if tipo_actual_arena == "normal":
                self.arena_actual = flujo_torneo.instanciar_arena("rocosa")
            elif tipo_actual_arena == "mojada":
                self.arena_actual = flujo_torneo.instanciar_arena("magnetica")
        else:  # derrumbe
            self.arena_actual = flujo_torneo.instanciar_arena("normal")
            self.metros_cavados -= METROS_PERDIDOS_DERRUMBE

        print(f"La arena final es del tipo {self.arena_actual.tipo}")
        for excavador in self.equipo_excavadores:
            excavador.felicidad -= FELICIDAD_PERDIDA
        print(f"Tu equipo ha perdido {FELICIDAD_PERDIDA} de felicidad\n")
