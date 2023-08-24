# Tarea 1: DCCavaCava 🏖⛏
## Consideraciones generales :octocat:
### Cosas implementadas y no implementadas :white_check_mark: :x:


#### Programación Orientada a Objetos: 42 pts (35%)
| Función             | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Diagrama      | ✅    | El diagrama de clases y su explicación en formato .md están disponibles en la carpeta "Diagrama".      |
| Definición de clases, atributos, métodos y properties     | ✅    | Todas las clases están correctamente definidas, así como sus métodos y sus properties.       |
| Relaciones entre clases     | ✅    | Por lo general, las clases acceden a atributos y métodos de otras clases ya instanciadas. Esto se da para la clase Torneo principalmente, que se conecta a instancias de excavadores e instancias de ítems y arenas.      |

#### Preparación programa: 11 pts (9%)
| Función             | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Creación de partidas      | ✅    | Al seleccionar la opción 1 del menú de inicio, se hace un llamado a ```flujo_torneo.nueva_partida()```, que crea las partidas e instancia lo necesario para aquello.        |

#### Entidades: 22 pts (18%)
| Entidad             | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Excavador      | ✅    | Se puede encontrar la clase en ```excavadores.py```, y la creación de la partida instancia la cantidad establecida en ```parametros.py```.       |
| Arena      | ✅    | Se puede encontrar la clase definida en ```arenas.py```, en conjunto con sus clases que le heredan.      |
| Torneo      | ✅    | La clase que maneja el torneo está en ```torneo.py```, mientras que las funciones que instancian las clases y generan las partidas se encuentran en ```flujo_torneo.py```.      |

#### Flujo del programa: 31 pts (26%)
| Función             | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Menú de Inicio      | ✅    | Se utiliza un menu manager en ```menu_utils.py``` que conecta los menú.       |
| Menú Principal      | ✅    | El menu manager de ```menu_utils.py``` es conectado a la instancia actual de la partida, tal que se crea un flujo funcional.     |
| Simulación día torneo      | ✅    | Se llama al método ```simular_dia()``` de la clase ```Torneo```, la que se encarga de hacer los print y de modificar los atributos correspondientes de la clase misma y las demás instancias.        |
| Mostrar estado torneo      | ✅    | Se llama a la función ```mostrar_estado()``` de la clase ```Torneo```, la que a su vez le entrega todos los datos necesarios a la función ```imprimir_estado_utils()``` de ```menu_utils.py```. No se integra al menu manager, ya que al no requerir input del usuario, se devuelve inmediatamente al menú principal.        |
| Menú Items      | ✅    | Se utiliza el menu_manager. La función ```ver_mochila()``` de ```Torneo``` retorna una lista que se le entrega a una función en ```menu_utils.py``` (```mostrar_menu_items(partida, lista)```), tal que se crea un menú con capacidad de regresar al principal.       |
| Guardar partida      | ✅    | Descripción más abajo.      |
| Robustez      | ✅    | Existe un amplio uso de clases y funciones que permiten una mayor cohesión y bajo acoplamiento.      |

#### Manejo de archivos: 14 pts (12%)
| Función             | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Archivos CSV      | ✅    | El módulo ```lectura_csv.py``` incluye todas las funciones necesarias para leer el CSV y trabajar con sus datos dentro del flujo del programa.     |
| Archivos TXT      | ✅    | El módulo ```manejo_txt.py``` trabaja con la lectura y el guardado de archivos en formato txt con encoding utf8.      |
| parametros.py      | ✅    | Se hace uso de todos sus parámetros en las distintas clases y funciones.      |

#### Bonus: 3 décimas máximo
| Bonus             | Estado | Implementación detallada |  
|---------------------|--------|-------|
| Guardar partida(s)      | ✅    | La función ```guardar_partida(partida, archivo)``` de ```manejo_txt.py``` se encarga de guardar la partida instanciada en ```partida``` en el archivo ```Partidas/archivo.txt```.       |


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se crearon los siguientes archivos adicionales:

### Contienen clases
1. ```excavadores.py```
2. ```items.py```
3. ```arenas.py``` 
4. ```torneo.py``` 
### Contienen funciones
5. ```flujo_torneo.py```
6. ```lectura_csv.py```
6. ```manejo_txt.py```
7. ```menu_utils.py```

### Ya entregados
8. ```parametros.py```: No está de menos destacar que contiene los parámetros modificables y que tienen relación con la ejecución del programa. Además, se le agregaron dos parámetros fijos (```VOLVER```, ```SALIR```) que apoyan la ejecución del menú.


Como todos estos archivos corresponden a módulos, el detalle de su implementación se encuentra en el apartado de librerías propias, más abajo en este documento. 

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```choices(), sample(), choice()``` en ```lectura_csv.py```, ```torneo.py```; ```randint()``` en ```torneo.py```, ```random(), choices()``` en ```excavadores.py```.
2. ```__future__``` : ```annotations``` en ```menu_utils.py```, ```torneo.py``` 
3. ```os``` : ```os.path...()``` en ```menu_utils.py```, ```os.path.join(), os.listdir()``` en ```manejo_txt.py```
4. ```abc```: ```ABC``` en ```items.py```, ```excavadores.py```, ```arenas.py```.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```excavadores```: contiene las clases sobre los excavadores.
2. ```items```: contiene las clases sobre los tesoros y los consumibles.
3. ```arenas```: contiene las clases sobre los tipos de arenas.
4. ```torneo```: contiene la clase sobre el torneo, en donde se produce el flujo principal de la competencia.
5. ```flujo_torneo```: contiene las funciones que instancian las clases necesarias para el flujo del torneo, así como las que inicializan una partida.
6. ```lectura_csv```: contiene las funciones necesarias para la lectura de los archivos csv y la extracción de datos de los mismos.
7. ```manejo_txt```: contiene las funciones necesarias para la lectura y creación de archivos .txt correspondientes a la carga y guardado de partidas respectivamente.
8. ```menu_utils```: contiene todas las funciones que manejan el uso de menú.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se asume que los nombres, tipos y descripciones de cada ítem no superarán los 30, 10 y 65 carácteres respectivamente. Esto se debe a que utilizamos contenidos de la semana 0 para hacer un print de un menú aesthetic.

2. Las edades jamás superaran los 60 años, ni disminuirán de los 18. Alguien que tiene 60 años y envejece, se mantendrá en la edad de 60.

3. Al abrir un tesoro que agregue miembros, SÍ se podrán repetir (pueden existir dos miembros distintos pero con el mismo nombre).

3. Al crear una partida, se instancian excavadores que no debiesen repetirse, lo que se consigue usando ```sample()```. 

4. Un excavador podrá entrar en descanso sólo al término de un día: es decir, si al final del día se encuentra que su energía es nula, se llamará a que este descanse. Esto significa que aquellos excavadores cuya energía sea nula luego de consumir un ítem, podrían ser puestos en descanso una vez que se simule un día. 

5. Al momento de consumir algo, se aplica para todos los excavadores. Sin embargo, aquellos excavadores que se encuentren descansando no dejarán de hacerlo por un aumento en la energía: los excavadores seguirán descansando hasta que transcurran los días establecidos, independiente de si su energía se ve aumentada por efectos de un ítem.

6. Al finalizar de descansar (trascurridos los días), el excavador vuelve a tener energía completa (100).

7. En la arena normal, la dificultad es ponderada por ```POND_ARENA_NORMAL``` cada vez que se simula un día, ya que es ese el momento de cavar. No está de más el mencionar que se redondea a los 2 decimales por medio del setter del atributo dificultad. 

8. El método ```encontrar_item()``` de la clase excavador recibe como parámetro el tipo de arena, de modo que si es mojada o magnética, la probabilidad de encontrar ítems (y su respectivo tipo) es distinta.

9.  El método ```gastar_energia()``` de excavador tiene la opción (por medio de un kwarg) de que se especifique que se trata un excavador híbrido. Cuando el excavador es híbrido, esta función se asegura de que la energía del excavador no descienda de las 20.

10. Se asume que la dificultad de la arena nunca alcanzará exactamente 0. Para prevenir crasheo por ZeroDivision, el setter ```dificultad``` de la clase ```Arena``` redondeará la dificultad a 0.01 cada vez que ```round(dificultad_nueva, 2) == 0.00```. 
11. Lo anteriormente mencionado puede ocurrir porque se tiene el supuesto de que una arena del tipo ```normal``` es ponderada por ```POND_ARENA_NORMAL``` cada vez que se simula un día (al comienzo, antes de comenzar a excavar).

12. Siempre se podrá abrir un tesoro que cambie el tipo de arena, incluso si la arena anterior era del mismo tipo.

13. Cuando se selecciona la opción de cargar partida y NO hay partidas, el programa cerrará.

14. En excavadores.csv, hay excavadores como Lily cuya suerte inicial es 0. Para corregir este problema, se llama inmediatamente a los setters de la clase ```Excavador``` una vez que esta es instanciada (líneas 23 a 29 de ```excavadores.py```). Para el resto de clases, se asume que todos los valores entregados en los archivos ```.csv.``` son válidos y coherentes, de tal forma que no pasan por los setters al ser instanciados por primera vez.

15. El valor de metros cavados SÍ puede ser negativo, producto de los derrumbes.

16. El torneo continuará incluso si se alcanza la meta antes de cumplir los días.
17. Los ítems SÍ se podrán repetir.


### Formato de guardado de partidas
Las partidas son guardadas en un archivo .txt dentro de la carpeta Partidas. Para facilitar la corrección, se puede considerar que existen 5 tipos de líneas a encontrar dentro de esto archivos:
1. ```CONSUMIBLE;nombre,descripcion,energia,fuerza,suerte,felicidad```.
2. ```TESORO;nombre,descripcion,calidad,cambio```.
3. ```EXCAVADOR;tipo,nombre,edad,energia,fuerza,suerte,felicidad,descansando,dias_descanso,dias_transcurridos_descanso```.
4. ```ARENA;tipo,nombre,rareza,humedad,dureza,estatica,dificultad```.
5. ```TORNEO;meta,cavado,dias_transcurridos,dias_totales```.


La idea de este formato es que el programa lea los elementos necesarios (y los instancie con sus respectivas clases) antes de instanciar Torneo y cargarlo. Además, es importante notar que al guardar una partida, se guardará también la meta.
Lógicamente, se asume que sólo habrá un elemento del tipo arena y un elemento del tipo torneo (en caso de que se desee crear un archivo de partida de forma manual).

:octocat: **En la carpeta ```Partidas```, podrán encontrar partidas simuladas que han sido guardadas :3**

### ☠️ PARTIDA EXPERIMENTAL ☠️ 

![Puppycat](https://media.tenor.com/MFfJSceYKRQAAAAC/puppycat-bee.gif)

Existe una partida experimental que ha sido incluida. Esta partida tiene como objetivo el cargarla para experimentar con la implementación de las properties, y contiene consumibles que no existen en ```consumibles.csv``` (¡son inventados dentro del ```.txt```!), pero que tienen la capacidad de ser superpoderosos. Es interesante notar como uno de los excavadores híbridos (```Hatsune Miku```) tiene arbitrariamente una energía igual a 0 dentro del archivo, la que luego se carga como energía igual a 20 en la partida, reflejando así la implementación de la property para los excavadores híbridos.

***La inclusión de esta partida es meramente con fines de apoyo para la evaluación. Ha sido escrita de forma manual, y contiene elementos absolutamente inventados, desde excavadores hasta arena y consumibles. Recomiendo que se observe el archivo primeramente si es que se desea cargar esta partida. El resto de partidas disponibles SÍ han sido guardadas por el programa a partir de simulaciones anteriores.***

-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<[Sala de Ayuda T1 – Menús – IIC2233 Syllabus](https://github.com/IIC2233/Syllabus/blob/main/Tareas/T1/Sala%20Ayuda/Sala%20Ayuda%20-%20Menus.ipynb)>: Se implementó el ```menu_manager()``` en la línea 248 de ```menu_utils.py```. Así mismo, todas las funciones que tienen relación a los menús y que se incluyen en el archivo previamente mencionado están inspirados en los ejemplos de esta sala de ayuda. La utilidad de esto es que permite tener un adecuado flujo de menús sin provocar recursión infinita.

2. \<[Sala de Ayuda T1 – Probabilidades – IIC2233 Syllabus](https://github.com/IIC2233/Syllabus/blob/main/Tareas/T1/Sala%20Ayuda/Sala%20Ayuda%20-%20Probabilidades.ipynb)>: Una buena parte de los elementos probabilísticos de la tarea fueron inspirados en esta sala de ayuda. Estos corresponden a: líneas 75, 144 a 148 de ```torneo.py```; línea 24 de ```lectura_csv.py```; líneas 120 a 129 de ```excavadores.py```. Todos los elementos implementados corresponden a ```random()``` y ```choices()```, y permiten extraer con métodos probabilísticos ciertas muestras, o bien, corroborar si se cumple una probabilidad específica.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
