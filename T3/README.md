# Tarea 3: DCCachos 🎲 🃏


## Consideraciones generales :octocat:
### Cosas implementadas y no implementadas :white_check_mark: :x:



#### Networking: 18 pts (16%)
| Networking                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Protocolo | ✅   | El protocolo TCP está implementado del lado del cliente y el servidor, en `cliente/backend/cliente.py` y `servidor/main.py` respectivamente. |
| Correcto uso de sockets | ✅   | Se hace uso de sendall (por medio de la función `enviar_informacion()` en `servidor/juego.py` y  `cliente/backend/cliente.py`) y recv (en `cliente/backend/cliente.py` y `servidor/main.py`).  |
| Conexión | ✅   | La conexión de un cliente se maneja en las líneas 81 en adelante en `servidor/main.py`.  |
| Manejo de Clientes | ✅   | El manejo de las clientes se maneja en `servidor/juego.py` por medio de `aceptar_jugador(), añadir_cliente()`.   |
| Desconexión Repentina | ✅   | Se gestionan diversos errores que permiten detectar las desconexiones repentinas (como paquetes de largo 0). La función que se suele llamar es `desconectar_cliente()` en `servidor/juego.py`, línea 175.   |
#### Arquitectura Cliente - Servidor: 18 pts (16%)

| Arquitectura Cliente - Servidor                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Roles | ✅   | Los roles están bien implementados, considerando que el frontend sólo notifica al backend de acciones, y recibe los cambios que el backend le ordena realizar (para actualizar lo visual). El backend gestiona todo lo correspondiente al flujo del juego.  |
| Consistencia | ✅   | Existe consistencia la arquitectura cliente-servidor. Como se describió anteriormente, los roles están bien separados y se mantienen de forma consistente.  |
| Logs | ✅   | Si bien los logs pueden imprimirse más de una vez por llamados múltiples a través del programa, en general, funcionan adecuadamente y permiten entender el flujo de lo que está aconteciendo en el programa.  |

#### Manejo de Bytes: 26 pts (22%)
| Manejo de Bytes  | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Codificación | ✅   | Esta función se encuentra en `[PATH]/Scripts/encoding.py`, donde PATH es `servidor` o `cliente`.  |
| Decodificación | ✅   | Esta función se encuentra en `[PATH]/Scripts/encoding.py`, donde PATH es `servidor` o `cliente`.  |
| Encriptación | ✅   | Esta función se encuentra en `[PATH]/Scripts/cripto.py`, donde PATH es `servidor` o `cliente`. *Se ha utilizado un valor de N fijo en parámetros.*  |
| Desencriptación | ✅   | Esta función se encuentra en `[PATH]/Scripts/cripto.py`, donde PATH es `servidor` o `cliente`. *Se ha utilizado un valor de N fijo en parámetros.*  |
| Integración | ✅   | El encriptado, codificación y demases se encuentran implementados con ayuda de las funciones `obtener_objeto_encriptado(), desencriptar_objeto()` ubicadas en el módulo `auxiliares` que se encuentran tanto para el cliente como para el servidor (son idénticas para ambos). Todos los elementos se encriptan y codifican antes de enviar, y se decodifican y desencriptar al momento de ser recibidos. |


#### Interfaz Gráfica: 22 pts (19%)
| Interfaz                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Ventana de Inicio | ✅   | La ventana de inicio está implementada, con su código fuente en `cliente/frontend/ventana_inicio.py`. Sus conexiones se encuentran en `cliente/main.py`.  |
| Ventana de Juego | ✅   | La ventana de inicio está implementada, con su código fuente en `cliente/frontend/ventana_juego.py`. Sus conexiones se encuentran en `cliente/main.py`.  |

Los elementos de la interfaz gráfica son apoyados por los módulos `alertas.py` e `iconos.py`, ambos ubicados en las respectivas carpetas de `[SERVIDOR/CLIENTE]/frontend`.

#### Reglas de DCCachos: 22 pts (19%)
Todo el flujo del juego está en `T3/servidor/juego.py`.
| Reglas de DCCachos         | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Inicio del juego | ✅   | El inicio del juego está permitido y se rellenan con bots cuando no hay suficientes jugadores.  |
| Bots | ✅   | Los bots actúan respetando las probabilidades y cumpliendo con las reglas del juego.  |
| Ronda | ✅   | Las rondas se reinician cuando es correspondiente y respetando los órdenes de los turnos.  |
| Término del juego | ✅   | El juego termina cuando se cumplen las distintas condiciones, notificando a los usuarios cuando es correspondiente.  |


#### Archivos: 10 pts (9%)
| Archivos                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Parámetros JSON | ✅   | Se encuentran los archivos `parametros.json` tanto en `cliente` como en `servidor`.
| main.py | ✅   | Ambos `main.py` piden el puerto para inicializar.   |
| cripto.py | ✅   | `cripto.py` se ubica en las carpetas `[CLIENTE/SERVIDOR]/Scripts` y son archivos idénticos.  |


#### Bonus: 4 décimas máximo
| Bonus                | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Cheatcodes | ❌   | Preferí dormir :C  |
| Turno con tiempo | ❌   | Preferí dormir :C  |


## Ejecución :computer:
### Servidor
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se crearon los siguientes archivos:
1. ```auxiliares.py```
2. ```juego.py```
3. ```jugador.py```
4. ```encoding.py``` en ```Scripts```
5. ```cripto.py``` en ```Scripts``` 

### Cliente
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se crearon los siguientes archivos:
1. ```auxiliares.py```
2. ```encoding.py``` en ```Scripts```
3. ```cripto.py``` en ```Scripts``` 
4. ```cliente.py``` en ```backend```
5. ```ventana_juego.py``` en ```frontend```
6. ```ventana_inicio.py``` en ```frontend```
7. ```alertas.py``` en ```frontend```
8. ```iconos.py``` en ```frontend```

**La carpeta `Sprites` debe ser ubicada dentro de la carpeta `cliente` para un adecuado funcionamiento.**

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```json```: En los archivos ```[CLIENTE/SERVIDOR]/auxiliares.py```.
2. ```pickle```: En los archivos ```[CLIENTE/SERVIDOR]/auxiliares.py```, ```[CLIENTE/SERVIDOR]/Scripts/encoding.py```.
3. ```os```: En los archivos ```cliente/frontend/iconos.py, cliente/frontend/ventana_juego.py, cliente/frontend/iconos.py```.
4. ```sys```: En los archivos ```[CLIENTE/SERVIDOR]/main.py```.
5. ```socket```: En los archivos ```cliente/backend/cliente.py```, ```servidor/juego.py```, ```servidor/main.py```.. 
6. ```PyQt5```: En los archivos ```cliente/main.py```, ```cliente/backend/cliente.py```, y todos los de ```cliente/frontend```.
7. ```time```: En los archivos ```servidor/juego.py``` y ```servidor/jugador.py```.
8. ```threading```: En los archivos ```servidor/main.py```, ```cliente/backend/cliente.py```, ```servidor/juego.py```.
9. ```random```: En los archivos ```servidor/jugador.py```, ```servidor/juego.py```.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
### Cliente
1. ```auxiliares```: Contiene las funciones que sirven como apoyo para diversas tareas dentro del cliente.
2. ```frontend.alertas```: Contiene la función necesaria para mostrar una alerta al cliente.
3. ```frontend.iconos```: Contiene clases que corresponden a los dados e íconos de los usuarios (que heredan de QLabel) con sus respectivos métodos.
4. ```frontend.ventana_inicio```: Contiene la ventana de inicio y sus elementos.
5. ```frontend.ventana_juego```: Contiene la ventana de juego y sus elementos.
6. ```Scripts.cripto```: Contiene las funciones necesarias para la encriptación y desencriptación.
7. ```Scripts.encoding```: Contiene las funciones necesarias para la codificación y decodificación.


### Servidor
1. ```auxiliares```: Contiene funciones que sirven como apoyo para diversas tareas del servidor.
2. ```juego```: Contiene la clase `Juego`
3. ```jugador```: Contiene la clase `Jugador` que es utilizada para el manejo de clientes, vidas, etcétera. 
4. ```Scripts.cripto```: Contiene las funciones necesarias para la encriptación y desencriptación.
5. ```Scripts.encoding```: Contiene las funciones necesarias para la codificación y decodificación.


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
1. Se asume que **siempre** se hará uso de puertos superiores a 1024. La explicación de esto se encuentra en el [siguiente link](https://stackoverflow.com/questions/25709716/socket-error-errno-13-permission-denied-when-creating-a-fake-email-server).
2. Se asume que los nombres de usuario jamás superarán los 14 dígitos (dentro de los parámetros definidos).
3. Se asume que el cliente y el servidor tendrán **siempre** el mismo ponderador dentro de sus parámetros. Si no son coincidentes, no se podrá ejecutar el programa.
4. Se asume que jamás se conectarán más de 8 clientes.
5. Si se desconecta la persona a la que le correspondía jugar, entonces se pasará de turno automáticamente, sin considerar a este jugador como el turno anterior.
6. Un jugador no podrá dudar de turno si es que el jugador del turno anterior ha muerto.
7. Cuando no quedan jugadores vivos (que no sean bots), la partida se termina automáticamente.
8. Si un bot quiere anunciar un valor pero no es estrictamente mayor al anteriormente anunciado, entonces pasa automáticamente.
9. Si un bot es quien comienza una ronda, éste no podrá dudar.
10. Se asume que el parámetro `numero_jugadores` (en cliente y servidor) será 4 y jamás se alterará. 
11. Se asume que el parámetro `numero_vidas` estará **siempre entre 1 y 6**, dado que se utilizan dados para representarlo. (servidor).
12. Existen los parámetros `cooldown_bots` y `tiempo_ver_dados`, en donde el primero representa el tiempo que esperan los bots antes de actuar, y el segundo representa el tiempo por el cual serán visibles los dados para el resto de jugadores.
13. Cuando finaliza la partida, los otros jugadores en espera podrán iniciar una nueva. Quienes estaban jugando la partida serán desconectados automáticamente.

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. <[Geeksforgeeks](https://www.geeksforgeeks.org/print-colors-python-terminal/)>: Se utiliza en `servidor/auxiliares.py` para imprimir mensajes con colores a la consola.
2. \<[Mi propia tarea 2 XD](https://github.com/IIC2233/tomastrivino-iic2233-2023-1/blob/d597cbedc3b7fe74356904854973bbf7dbeea582/Tareas/T3/cliente/frontend/alertas.py#L5)>: Se utiliza en `cliente/frontend/alertas.py` para gestionar las alertas que se le muestran al jugador.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
