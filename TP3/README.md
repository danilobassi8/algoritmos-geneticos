# Trabajo Practico N° 3

## Problema del viajante

El problema del viajante (también conocido como problema del viajante de comercio o por sus siglas en inglés: TSP (Traveling Salesman Problem), es uno de los problemas más famosos (y quizás el mejor estudiado) en el campo de la optimización combinatoria computacional.

A pesar de la aparente sencillez de su planteamiento, el TSP es uno de los más complejos de resolver .

Definición: Sean N ciudades de un territorio. La distancia entre cada ciudad viene dada por la matriz D: NxN, donde d[x,y] representa la distancia que hay entre la ciudad X y la ciudad Y.

El objetivo es encontrar una ruta que, comenzando y terminando en una ciudad concreta, pase una sola vez por cada una de las ciudades y minimice la distancia recorrida por el viajante.


### Ejercicios:

* 1 - Hallar la ruta de distancia mínima que logre unir todas las capitales de provincias de la República Argentina, utilizando un método exhaustivo. ¿Puede resolver el problema?
* 2 - Realizar un programa que cuente con un menú con las siguientes opciones: 
  * a) Permitir ingresar una provincia y hallar la ruta de distancia mínima que logre unir todas las capitales de provincias de la República Argentina partiendo de dicha capital utilizando la siguiente heurística: “Desde cada ciudad ir a la ciudad más cercana no visitada.”  Recordar regresar siempre a la ciudad de partida. Presentar un mapa de la República con el recorrido indicado. Además   indicar la ciudad de partida, el recorrido completo y la longitud del trayecto. El programa deberá permitir seleccionar la capital que el usuario desee ingresar como inicio del recorrido.
  * b) Encontrar el recorrido mínimo para visitar todas las capitales de las provincias de la República Argentina siguiendo la heurística mencionada en el punto a. Deberá mostrar como salida el recorrido y la longitud del trayecto.
  * c) Hallar la ruta de distancia mínima que logre unir todas las capitales de provincias de la República Argentina, utilizando un algoritmo genético.



#### Recomendaciones de la catedra para el algoritmo genético :

* N = 50 Número de cromosomas de las poblaciones.
* M = 200 Cantidad de ciclos.
* Cromosomas: permutaciones de 23 números naturales del 1 al 23 donde cada gen es una ciudad.
* Las frecuencias de crossover y de mutación quedan a criterio del grupo.
* Se deberá usar crossover cíclico.
* Comparar los resultados obtenidos  entre la resolución a través de heurísticas y con algoritmos genéticos a través de una conclusión que deberá anexarse al informe.
* Agregar en el informe un apartado final denominado «Aportes Prácticos del TSP» donde se expliquen algunas aplicaciones en las que actualmente se use el problema del viajante. Tomar por lo menos dos y explicarlas.