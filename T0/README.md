# Tarea 0: DCCeldas 💣🐢🏰
## Consideraciones generales :octocat:

El programa entrega un menú de acciones funcional que trabaja con el archivo que se es ingresado inicialmente. Tiene la capacidad de verificar el cumplimiento de las reglas del juego y de solucionar tableros cuando esto sea posible, aunque tiende a ser más rápido con tableros inferiores a 7x7. Por temas de memoria, los tableros grandes tienden a tardar más en ser corregidos, pero sigue dando como resultado algo funcional.

### Cosas implementadas y no implementadas :white_check_mark: :x:

- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Menú de Inicio (5 pts) (7%)
| Menú                | Estado | Notas |  
|---------------------|--------|-------|
| Seleccionar archivo | ✅   |      |
| Menú de inicio      | ✅   |       | 
#### Menú de Acciones (11 pts) (15%) 
| Menú             | Estado | Notas |  
|---------------------|--------|-------|
| Opciones                  | ✅   |       |
| Mostrar tablero           | ✅   |       | 
| Validar bombas y tortugas | ✅   | Verifica también cumplimiento de la regla 5 (bonus).        | 
| Revisar solución          | ✅   |       | 
| Solucionar tablero        | ✅   | Funciona rápidamente para tableros pequeños. Si el tablero no se puede solucionar o ya está solucionado, notifica al usuario.        | 
| Salir                     | ✅   |       | 

#### Funciones (34 pts) (45%)
| Función             | Estado | Notas |  
|---------------------|--------|-------|
| Cargar tablero     | ✅   |       |
| Guardar tablero    | ✅   |   | 
| Valor bombas       | ✅   |       | 
| Alcance bomba      | ✅   |       | 
| Verificar tortugas | ✅   |        | 
| Solucionar tablero | ✅   | Funciona rápidamente para tableros pequeños.       | 

#### General: (19 pts) (25%)
| General             | Estado | Notas |  
|---------------------|--------|-------|
| Manejo de Archivos  | ✅   |        |
| Menús               | ✅   | Es consistente con el input.     | 
| tablero.py          | ✅   | Se utiliza el módulo en ```menu_utils.py```.      | 
| Módulos             | ✅   |       | 
| PEP-8               | ✅   | Se ha verificado por medio de flake8 su cumplimiento.      | 

#### Bonus: 6 décimas
| BONUS :D             | Estado | Notas |  
|---------------------|--------|-------|
| Funciones atómicas  | ✅   | Todas las funciones tienen máximo 15 líneas. |
| Regla 5             | ✅   |       | 

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se crearon los siguientes archivos:
1. ```menu_utils.py``` en ```carpeta base (T0)```: contiene todas las funciones que apoyan el flujo del programa y que son llamadas por medio de ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```menu_utils.py```, para asegurar que el archivo exista y manejar paths.
1. ```copy```: ```functions.py```, para hacer una copia profunda de la lista tablero en la función que es para solucionarla, de esta manera no se alteran los valores del tablero original.


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```menu_utils```: Contiene todo lo importante del flujo principal, ayuda a verificar existencia de archivos, usar os.path.join para evitar errores, y también cuenta con funciones como ```obtener_archivo_inicio()```, ```menu_acciones(archivo)``` etc., que son las llamadas en ```main.py```como parte del flujo inicial.
1. ```alcance_utils```: Contiene funciones como ```alcance_x(tablero, x, y)```, que sirven como apoyo para verificar los alcances (y listas de alcances) desde bombas y tableros, y se incluye en este módulo para evitar redudancia. Son exclusivamente de apoyo y usadas en ```functions.py```.



## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Asumí que el input correspondiente al archivo es SIEMPRE ```nombre.txt```, el que será buscado en el path relativo ```Archivos/nombre.txt```. Esto fue aclarado en las issues de la T0 del curso.
2. Se asume que, en caso de que el usuario entregue un input innecesario en el menú (por ejemplo "A" en vez de "1"), será necesario insistir en vez de cerrar el programa. Por esto, cuando se ingresa un input inesperado dentro del menú, se procede a insistirle al usuario que recuerde ingresar una de las opciones adecuadas del menú.
3. En el bonus de las islas, asumí que también debe cumplirse la regla 5 para la opción 2 del menú.
4. Es importante considerar que si se ingresa un tablero ya solucionado y luego se solicita solucionar el mismo (opción 4), el programa devolverá el tablero inicial, SIN CREAR UN ARCHIVO NUEVO, y se notificará al usuario que está intentando solucionar un tablero que ya cumple con todo.
5. A pesar de que se escoja la opción 4 y se solucione un tablero, el flujo del menú seguirá trabajando con el tablero original. Esto quiere decir que, si se ingresa la opción 4 (solucionar) e inmediatamente después la opción 1 (ver tablero), se imprimirá el tablero original en la consola.
-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<[Sala de Ayuda T0 – IIC2233 Syllabus](https://github.com/IIC2233/Syllabus/tree/main/Tareas/T0/Sala%20Ayuda)>: se implementaron las funciones recursivas basadas en las del código de ```laberinto.py```. Se pueden encontrar en ```functions.py``` en las líneas 270 (función ```es_valida(tablero: list, posicion: tuple, ruta_actual: list) -> bool```) y 285 (función ```obtener_tabla(tablero: list, camino: list) -> list```) y tienen como función el verificar que la posición a probar sea correcta y el encontrar una tabla solucionada respectivamente. Si bien el código no es exactamente igual, sí está basado a partir del anteriormente mencionado y su funcionamiento es prácticamente el mismo.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
