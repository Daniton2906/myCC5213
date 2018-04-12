Tarea 1 - Daniel Diomedi

Info versiones usadas relevantes:
Python 3.6.5
OpenCV 3.4.0
matplotlib 2.2.2
numpy 1.14.2
scipy 1.0.1

Como ejecutar tarea (el archivo main.py ejecuta el programa)
1. Mover datos dentro de carpeta data como se ilustra a continuacion
	|
	|/data
	   |/data/television
	   |/data/comerciales
	|/src
	|/tools
	|main
   Mantener nombres de carpetas television y comerciales (pls c:)

2. Ejecutar en terminal: python main.py (también se puede importar proyecto a PyCharm y correr main.py dentro del programa)

3. Se preguntará si se desea ejecutar programa completo (Poner 1 si se quiere hacer eso, si no apretar solo Enter). Saltar a paso 5

4. Si elige que no (solo quieres ejecutar una parte), puede ingresar secuencia de 1s o 0s dependiendo que parte del programa se quiere ejecutar
	- Primera posicion: Calcular descriptores de comerciales según parte 1 descrita en enunciado
	- Segunda posicion: Calcular descriptores de comerciales según parte 1 descrita en enunciado
	- Tercera posicion: Calcular k cuadros más cercanos (knf) según parte 2 descrita en enunciado
	- Cuarta posicion: Detectar comerciales y escribir resultados según parte 3 descrita en enunciado

   Cualquier otra secuencia extra será ignorada. Ejemplo: 0011, solo calcula KNFs y detecta colisiones.

5. Al final, se generará archivo results.txt en carpeta /data/results/

*Notar que según, como se guardan datos en memoria secundaria, se crean carpetas temporales con esta información. 