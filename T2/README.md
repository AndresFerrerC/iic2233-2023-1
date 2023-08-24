# Tarea 2: DCCazafantasmas 👻🧱🔥
![nintendo](https://i.imgur.com/U6pQYVT.png)
## Consideraciones generales :octocat:
### Esta tarea fue hecha y probada en un Macbook Air M1. Desconozco cómo se comporte el programa con otro S.O. o arquitectura de CPU. :(
### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Ventanas: 27 pts (27%)
| Ventanas                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Ventana de Inicio | ✅   | El frontend de la ventana de inicio se puede encontrar en `frontend/ventana_inicio.py`. Contiene señales que están conectadas al flujo de `backend/backend_inicio.py`. *[Verificación de nombre: `backend/backend_inicio.py` línea 15. Selector de mapas en `frontend/ventana_inicio.py` línea 88, que llama a la función de `auxiliares.py` ubicada en la línea 12. Cerrar programa: línea 117 de `frontend/ventana_inicio.py`.]*     |
| Ventana de Juego | ✅   | El frontend de la ventana de juego se puede encontrar en `frontend/ventana_juego.py`. Contiene señales que están conectadas al flujo de `backend/backend_juego.py`. Al finalizar el juego, se abre otra ventana cuyo código se encuentra en `frontend/ventana_fin.py`. *[La actualización del tiempo se gestiona por medio de señales ubicadas en `frontend/temporizador.py`, que se comunican con las del frontend de la ventana de juego. Por otra parte, se inicia el juego al presionar el botón jugar, lo que se verifica en el archivo `backend/backend_constructor.py` en la línea 112. Las otras estadísticas (vidas) se actualizan en el frontend en la línea 254, por medio de una señal emitida desde `backend/backend_juego.py`. Las señales están en definidas en las líneas 8 a 17 del archivo últimamente mencionado. ]*      |

#### Mecánicas de juego: 47 pts (47%)
| Mecánicas de Juego                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Luigi | ✅   | El apartado visual de Luigi se ubica en `frontend/frontend_luigi.py` y contiene una clase Luigi, que hereda de QLabel, que a su vez tiene métodos que permiten la animación del personaje. El backend se encuentra en `backend/luigi.py` y contiene información básica para instanciar el personaje y trabajarlo dentro del backend del juego. Todo el backend del flujo del juego, que controla a Luigi, se encuentra en `backend/backend_juego.py`.   *[Las colisiones y el movimiento, así como la muerte del personaje, se manejan en las líneas 142, 231 y 286 del backend del juego. Se permite el uso de las teclas en la línea 207 del frontend del juego. ]*  |
| Fantasmas | ✅   | El frontend de los fantasmas se encuentra en `frontend/frontend_objetos.py` y también contiene clases de los respectivos fantasmas, así como sus métodos para ser animados y demás. Son controlados por el backend en `backend/backend_juego.py`, en donde se crean sus respectivas instancias del backend que se pueden encontrar en `backend/fantasmas.py`. Este último archivo contiene las clases del backend de los fantasmas, métodos y timers que permiten su movimiento.  *[La función que define el movimiento aleatorio de los fantasmas está en `backend/fantasmas.py`, línea 20. ]*    |
| Modo Constructor | ✅   | El frontend se encuentra en `frontend/ventana_juego.py`. El backend se ubica en `backend/backend_constructor.py`, lo que se complementa con `backend/backend_inicio.py` (esto último como apoyo para inicializar la ventana del juego desde el constructor).    |
| Fin de ronda | ✅   | El fin de la ronda está gestionado desde `backend/backend_juego.py` y se abre una ventana ubicada en `frontend/ventana_fin.py`.      |

#### Interacción con el usuario: 14 pts (14%)
| Interacción con el usuario                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Clicks | ✅   | Se permite uso de clicks en los botones y dropdowns dentro de las ventanas del juego. Por implementación de Drag and Drop, está deshabilitado en el selector de ítems dentro del constructor, lo que se autorizó en la [issue a continuación](https://github.com/IIC2233/Syllabus/issues/358#issuecomment-1555943299).    |
| Animaciones | ✅   | Las animaciones se encuentran implementadas con timers y `QPropertyAnimation` dentro de las clases de los personajes pertenecientes al frontend, cuyas rutas fueron mencionadas anteriormente.     |
#### Funcionalidades con el teclado: 8 pts (8%)
| Funcionalidades con el teclado                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Pausa | ✅   | Se permite la pausa con la tecla P dentro de la ventana de juego. También sirve para reanudar.  *[La detección de la pausa se ubica en la línea 218 de la ventana de juego. ]*   |
| K + I + L | ✅   | Se puede utilizar KIL cuando está iniciado el juego. Elimina los fantasmas *hasta que se resetea el mapa*.  *[Los atajos se establecieron en la línea 351 de la ventana de inicio. Su aplicación se ejecuta en el backend del juego por medio de señales que están conectadas en `main.py`.]*      |
| I + N + F | ✅   | Se puede utilizar INF cuando está iniciado el juego.      |
#### Archivos: 4 pts (4%)
| Archivos                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Sprites | ✅   | Se hace uso de los sprites para los íconos y pixmap a lo largo de todas las ventanas del juego.      |
| Parametros.py | ✅   | Se hace uso de `parametros` en los archivos del juego, tanto en backend como en frontend.     |
#### Bonus: 8 décimas máximo
| Archivos                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Volver a Jugar | ✅   | Al finalizar la partida, se abre una ventana de término de juego, el que tiene un botón que permite volver a jugar. Se reinicia el tiempo, la cantidad de vidas y todo vuelve a su posición original.   |
| Follower Villain | ✅  | Se ha implementado un follower villain, con sus clases de frontend y backend ubicados en los mismos archivos que los del resto de fantasmas. El fantasma persigue a Luigi para quitarle una vida. |
| Drag and Drop | ✅   | Se ha implementado el Drag and Drop en el selector y puede encontrarse su uso en `frontend_ventana_juego.py`, en donde se instancia la clase del botón movible (botón que puede tener drag and drop) ubicada en el archivo `frontend/drag_and_drop.py`.     |

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además, se crearon los siguientes archivos:
### Carpeta base
1. ```auxiliares.py```
### Carpeta Backend
1. ```backend_constructor.py```
2. ```backend_inicio.py```
3. ```backend_juego.py```
4. ```fantasmas.py```
5. ```luigi.py```
6. ```objetos.py```
### Carpeta Frontend
1. ```drag_and_drop.py```
2. ```frontend_luigi.py```
3. ```frontend_objetos.py```
4. ```reproductor.py```
5. ```temporizador.py```
6. ```ventana_fin.py```
7. ```ventana_inicio.py```
8. ```ventana_juego.py```

**Las carpetas `sprites`, `mapas` y `sounds` deben ser ubicadas en la carpeta base, es decir, en la misma carpeta en que se ubica el archivo `main.py`.**
Las explicaciones en detalle se encuentran en el apartado de librerías propias.
## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: En los archivos `auxiliares.py`, `backend/backend_constructor.py`, `frontend/frontend_luigi.py`, `frontend/frontend_objetos.py`, `frontend/reproductor.py`, `frontend/ventana_fin.py`, `frontend/ventana_inicio.py`.
2. ```PyQt5```: En todos los archivos de backend y frontend.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```frontend.frontend_luigi```: Contiene la clase `Luigi` del frontend (hereda de QLabel).
2. ```frontend.frontend_objetos```: Contiene todas las clases (heredan de QLabel) de los objetos y entidades externas a Luigi, algunas con métodos que permiten su animación (como los fantasmas).
3. ```frontend.drag_and_drop```: Contiene la clase `BotonMovible`, que tiene la característica de permitir Drag and Drop. Permite el habilitar drag and drop en el constructor.
4. ```frontend.reproductor```: Contiene la clase `Reproductor`, que permite la reproducción de audio dependiendo del tipo de evento `WIN/LOSS`. 
5. ```frontend.temporizador```: Contiene la clase `Temporizador` (hereda de QLabel) que maneja el contador de tiempo restante y se encarga de notificar el término de tiempo, así como de actualizar el tiempo en la ventana del juego.
6. ```frontend.ventana_inicio```: Crea la ventana de inicio y todos sus elementos.
7. ```frontend_ventana_juego```: Crea la ventana del juego y del constructor, así como todos sus respectivos elementos.
8. ```frontend_ventana_fin```: Crea la ventana del término del juego y sus elementos.
9. ```backend.backend_inicio```: Verifica que lo ingresado en la ventana de inicio sea correcto y autoriza iniciar el juego.
10.  ```backend.backend_constructor```: Maneja el flujo del constructor y permite la comunicación con el backend.
11. ```backend.backend_juego```: Maneja todo el flujo del inicio y del fin del juego, así como los personajes del mismo.
12. ```backend.fantasmas.py```: Contiene las clases del backend de todos los tipos de fantasmas.
13. ```backend_luigi.py```: Contiene la clase `Luigi` del backend.
14. ```backend.objetos```: Contiene las clases de los objetos ajenos a Luigi y a los fantasmas dentro del backend.
15. ```auxiliares```: Se ubica en la carpeta base y contiene funciones que son utilizadas tanto por el backend como el frontend. Permite evitar código redundante dentro de los archivos.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:


1. El constructor no permite poner fantasmas encima de otros, a pesar de que se puedan superponer durante el transcurso del juego.
2. La grilla (o el tablero) se trabaja principalmente con posiciones relativas y no absolutas dentro del mapa. Es decir, con posiciones como `(0, 0)`, en vez de `(32, 32)`. Esto es para comprender de mejor manera dónde se ubican los elementos.
3. Los movimientos y sprites predeterminados de los fantasmas son: dirección derecha para los fantasmas `verticales, horizontales y follower`, y arriba para el fantasma vertical.
4. Para que Luigi pueda escapar en el caso en que se cree un mapa en donde este se encuentra inmediatamente arriba de un fantasma vertical (o a la derecha de un horizontal), implementé un `COOLDOWN_FANTASMAS` en parámetros. Por esta razón, al iniciar (o reiniciar, pero no resetear) una partida, los fantasmas comenzarán a moverse transcurridos `COOLDOWN_FANTASMAS`. Para evitar esta situación, el parámetro puede setearse a 0.
5. Se asume que los valores de la velocidad máxima y mínima serán coherentes, ojalá entre 1 y 2 y que ninguno será 0.
6. El tiempo de movimiento de los fantasmas se refiere a la cantidad de segundos que tienen que pasar antes de moverse de una casilla a otra, como se autorizó en [esta issue](https://github.com/IIC2233/Syllabus/issues/319#issuecomment-1552343464).
7. Si se pausa el juego mientras un personaje ejecuta un movimiento, entonces aquel personaje terminará de moverse a la siguiente casilla.
8. Cuando se reinicia un nivel desde la ventana de término, se reinicia la cuenta regresiva, de la misma forma en que se anulan los cheatcodes aplicados previamente.
9. Los villanos sí vuelven a aparecer una vez que se aplica el comando KIL y se resetea la partida (cuando Luigi toca fuego).
10. Para reproducir audio en `frontend/temporizador.py`, se hace uso de la función `os.abspath()` junto a `os.path.join()`. La implementación fue considerada **válida** por el profesor del curso y se encuentra su autorización en [este enlace](https://github.com/IIC2233/Syllabus/issues/290#issuecomment-1555942196).
11. En la ventana de inicio, se puede presionar la tecla enter en vez del botón ingresar. Ambos sirven.
12. En el caso de que se opte por jugar una nueva partida (reiniciar), el audio de ganar/perder terminará de reproducirse de todos modos.
13. El FollowerVillain escogerá a dónde moverse en función de la distancia con Luigi. En ciertos casos, podría moverse repetidamente entre una casilla y otra, lo que cambiará apenas Luigi comience a moverse nuevamente. La aprobación de este caso por parte de los profes se [encuentra aquí](https://github.com/IIC2233/Syllabus/issues/386).
14. Se asume que los parámetros `MAXIMO_LUIGI` y `MAXIMO_ESTRELLA` serán **siempre iguales a 1**.
15. Es importante destacar que, dependiendo del computador y otros factores, **el audio podría demorar unos segundos en reproducirse**. Por esto, se recomienda no cerrar inmediatamente la ventana del fin del juego.
16. Se asume que las teclas (WASD) no se presionarán de forma seguida, es decir, que habrá un intervalo de tiempo entre cada vez que se presiona una tecla.
17. Cuando un fantasma se mueve hacia Luigi, es posible que no alcance a verse la animación, ya que el mapa se reiniciará inmediatamente. 
18. El puntaje se calculará y mostrará incluso si es que se pierde la partida.
19. Si no se ocupa vida alguna (es decir, si se termina la partida con todas las vidas), el cálculo del puntaje se hará considerando 1 vida ocupada.
20. **Todas las señales (salvo la de actualizar el temporizador) están conectadas en `main.py` con breves explicaciones**.


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<[StackOverflow: Shortcuts](https://stackoverflow.com/questions/25989610/pyqt5-keyboard-shortcuts-w-qaction)>: Permitió usar QShortcuts dentro del frontend del juego.
2. \<[Youtube: Drag and Drop](https://www.youtube.com/watch?v=s1QZIwg3x3o)>: Permitió la implementación del Drag and Drop y puede encontrarse en `frontend/drag_and_drop.py`.
3. \<[TutorialsPoint: Drag and Drop](https://www.tutorialspoint.com/pyqt/pyqt_drag_and_drop.htm)>: Complementó la implementación del Drag and Drop mencionado anteriormente.
4. \<[StackOverflow: PyQt Countdown](https://stackoverflow.com/questions/62006303/pyqt-countdown-timer-in-mmss-format)>: Se utilizó como base para el temporizador del juego.
5. \<[StackOverflow: Clear Layout](https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt)>: Se implementó aquel código en la función `limpiar_layout()` dentro de `auxiliares.py`. Permite limpiar el layout para instanciar otros botones con valores actualizados.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).

## That's it!
![puppycat](https://media.tenor.com/Z3yEZw5KcV0AAAAC/bee-and-puppycat-puppycat.gif)


¡Lamento si se me pasó algo! Esta tarea fue un desafío gigante para mi persona y aprendí mucho. Espero que la disfrutes tanto como disfruté yo el ver un resultado final funcional.

![trabajo](https://i.pinimg.com/736x/8f/58/47/8f58471830178051ab6ed82382637f23.jpg)