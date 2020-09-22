import funciones_pantalla as fp
import datos
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import statistics
from tqdm import tqdm

# --------------------------- OPCIÓN UNO --------------------------- #


def greedy(inicial):
    recorrido = []
    distTotal = 0
    recorrido.append(inicial)

    provActual = inicial
    while (len(recorrido) < len(provincias)):
        # me traigo la proxima ciudad sin haber sido recorrida
        provProx, distMin = datos.CalculaProvMinDistancia(provActual, recorrido)
        distTotal += distMin
        recorrido.append(provProx)
        provActual = provProx

    # al terminar calculo la distancia entre el ultimo del recorrido y el inicial
    distTotal += datos.CalculaDistancia(inicial, recorrido[-1])
    # y agrego al inicial al final del recorrido
    recorrido.append(inicial)
    return recorrido, distTotal

# --------------------------- OPCION DOS --------------------------- #


def MejorRecorrido(provincias):
    distMin = math.inf
    recorridoMin = []

    for p in provincias:
        recorrido, distancia = greedy(p)
        if(distancia < distMin):
            distMin = distancia
            recorridoMin = recorrido
    return recorridoMin, distMin


# --------------------------- Algoritmo Genético --------------------------- #

def rellenarPoblacionInicial(cantCromosomas):
    poblacion = []

    for j in range(cantCromosomas):
        # relleno numeros del 1 al 24
        numeros = []
        for i in range(24):
            numeros.append(i)
        cromosoma = []
        for i in range(len(numeros)):
            # elijo un numero del arreglo numeros
            numero = random.choice(numeros)
            # agrego al cromosoma el numero seleccionado
            cromosoma.append(numero)
            # luego lo borro
            numeros.remove(numero)
        poblacion.append(cromosoma)

    return poblacion


def funcionObjetivo(recorrido):
    return datos.CalculaDistanciaDeRecorrido(recorrido)


def rellenarFuncionesObjetivoYFitness(poblacion):
    # rellenar F objetivo
    listaFObjetivo = []
    listaFitness = []
    arregloComplemento = []

    for i in range(len(poblacion)):
        listaFObjetivo.append(funcionObjetivo(poblacion[i]))

    # rellenar F fitness
    sumatotal = sum(listaFObjetivo)
    arregloComplemento = []
    for i in range(len(listaFObjetivo)):
        arregloComplemento.append(sumatotal - listaFObjetivo[i])

    sumatotal = sum(arregloComplemento)
    for i in range(len(poblacion)):
        listaFitness.append(arregloComplemento[i] / sumatotal)

    return listaFitness, listaFObjetivo


def seleccionarPareja(poblacion, listaFitness):
    pareja = []
    ruleta = []

    # genero la ruleta como un pool proporcional al fitness.
    ruleta.append(listaFitness[0])
    for i in range(1, len(listaFitness)):
        ruleta.append(listaFitness[i] + ruleta[i - 1])

    # elijo cada uno de los padres.
    for veces in range(2):
        r = random.uniform(0, 1)
        indice = 404

        for i in range(len(ruleta)):
            if i == 0:
                if(0 <= r <= ruleta[i]):
                    indice = i
                    break
            else:
                if(ruleta[i - 1] <= r <= ruleta[i]):
                    indice = i
                    break
        pareja.append(poblacion[indice])

    return pareja


def Crossover_Ciclico(p1, p2):

    # se copia para resolver problemas de referencias #
    hijo = p2.copy()
    indexP1 = 0
    sigue = True
    while(sigue):
        valorP1 = p1[indexP1]
        hijo[indexP1] = valorP1

        valorP2 = p2[indexP1]
        # actualizo el indice de 1
        indexP1 = p1.index(valorP2)

        if(valorP2 in hijo):
            sigue = False

    return hijo


def crossover(padres, prob):
    r = random.uniform(0, 1)
    if(r <= prob):
        hijo1 = Crossover_Ciclico(padres[0], padres[1])
        hijo2 = Crossover_Ciclico(padres[1], padres[0])
        return hijo1, hijo2
    else:
        return padres[0], padres[1]


def mutacion(hijoOriginal, prob):
    # hacemos una copia para que no ocurran problemas de referencias de Python
    hijo = hijoOriginal.copy()

    r = random.uniform(0, 1)
    if(r <= prob):
        indice1 = int(random.uniform(0, len(hijo)))
        indice2 = int(random.uniform(0, len(hijo)))

        vAux = hijo[indice1]
        hijo[indice1] = hijo[indice2]
        hijo[indice2] = vAux
    return hijo


def mostrarGraficasEnPantalla(ejeX, minimos, maximos, media, minHistorico):
    plt.plot(ejeX, minimos, label='Minimos', linewidth=4, color="red", alpha=0.6)
    plt.plot(ejeX, maximos, label='Maximos', linewidth=4, color="blue", alpha=0.6)
    plt.plot(ejeX, media, label='Media', linewidth=4, color="green", alpha=0.6)
    plt.plot(ejeX, minHistorico, label='Mejor Historico', linewidth=4, color="purple", alpha=0.2)

    plt.legend()
    plt.ylabel(' Valor de la Funcion Objetivo ')
    plt.xlabel(' Generación ')
    plt.show()


def elitismo(poblacion, listaFitness, cantElite):
    # Creamos una copia de la lista (Fitness u objetivo), elegimos el mejor, lo borramos
    # y volvemos a elegir el mejor. Luego sacamos los indices en el arreglo original.
    # y agregamos en la proximaGeneracion la poblacion en el indice de los mejores.

    indiceMejor = []
    copiaFitness = listaFitness.copy()
    elites = []

    for i in range(cantElite):
        mejor = min(copiaFitness)
        indiceMejor.append(listaFitness.index(mejor))
        copiaFitness.remove(mejor)

    for i in range(cantElite):
        elites.append(poblacion[indiceMejor[i]])

    return elites


def Genetico(provincias):
    poblacion = []
    proximaGeneracion = []

    # Lista F objetivo y F Fitness.
    listaFObjetivo = []
    listaFitness = []

    # Parametros.
    cantMaximaGeneraciones = 200
    cantIndividuosEnPoblacion = 50
    p_crossover = 0.9
    p_mutacion = 0.2

    # arreglos para las graficas.
    mostrarGraficas = True  # si no se quieren mostrar graficas de rendimiento poner en false.
    ejeX = []
    minimos = []
    maximos = []
    medias = []
    minHistorico = []

    hayElitismo = input("¿Aplicar elitismo? (s/n): ")
    if(hayElitismo.lower() == 's'):
        hayElitismo = True
        cantElite = 10
    else:
        hayElitismo = False
        cantElite = 0

    # inicializo poblacion y lista fitness
    poblacion = rellenarPoblacionInicial(cantIndividuosEnPoblacion)
    listaFitness, listaFObjetivo = rellenarFuncionesObjetivoYFitness(poblacion)

    # variables para guardar los mejores.
    distMinima = math.inf
    MejorRecorrido = []

    terminado = False
    cantidadCiclos = 0

    # esta linea es para que se muestre una barra de carga con ciertas opciones
    with tqdm(total=cantMaximaGeneraciones, ncols=60,
              bar_format="{desc}: >{percentage:.0f}%|{bar}| Generación: {n_fmt}/{total_fmt}") as barra:

        for i in range(cantMaximaGeneraciones):
            barra.update()

            cantidadCiclos += 1
            # aplica el ELITISMO
            if(hayElitismo):
                proximaGeneracion += elitismo(poblacion, listaFObjetivo, cantElite)

            for i in range(int((len(poblacion) - cantElite) / 2)):
                # seleccionar 2 individuos para el cruce
                padres = seleccionarPareja(poblacion, listaFitness)
                # cruzar con cierta probabilidad 2 individuos y obtener descendientes
                hijo1, hijo2 = crossover(padres, p_crossover)
                # Mutar con cierta probabilidad
                hijomutado1 = mutacion(hijo1, p_mutacion)
                hijomutado2 = mutacion(hijo2, p_mutacion)

                proximaGeneracion.append(hijomutado1)
                proximaGeneracion.append(hijomutado2)

            poblacion = proximaGeneracion.copy()
            proximaGeneracion = []
            listaFObjetivo = []
            listaFitness = []

            # rellena funcion fitness y objetivo.
            listaFitness, listaFObjetivo = rellenarFuncionesObjetivoYFitness(poblacion)

            # calculo el mejor
            menorDistancia = min(listaFObjetivo)
            if(menorDistancia <= distMinima):
                distMinima = menorDistancia
                MejorRecorrido = poblacion[listaFObjetivo.index(menorDistancia)]

            # guardo los arreglos para generar las graficas
            if(mostrarGraficas):
                # guardo los mejores, peores y la media de esta generacion
                ejeX.append(cantidadCiclos)
                minimos.append(min(listaFObjetivo))
                maximos.append(max(listaFObjetivo))
                medias.append(statistics.mean(listaFObjetivo))
                minHistorico.append(distMinima)

        if(mostrarGraficas):
            mostrarGraficasEnPantalla(ejeX, minimos, maximos, medias, minHistorico)

        return datos.mapearRecorrido(MejorRecorrido + [MejorRecorrido[0]]), datos.CalculaDistanciaDeRecorrido(MejorRecorrido)
# --------------------------- MAIN --------------------------- #


provincias = datos.provincias

print(" ----------------------------------------- ")
print(" 1 - Elegir provincia y realizar Heuristica")
print(" 2 - Mejor recorrido utilizando la Heuristica")
print(" 3 - Algoritmo Genético")
print(" ----------------------------------------- ")
op = input('Seleccione una opción: ')

if(op == '1'):
    provinciaInicial = fp.elegirProvincia()
    recorrido, distTotal = greedy(provinciaInicial)
if(op == '2'):
    recorrido, distTotal = MejorRecorrido(provincias)
if(op == '3'):
    recorrido, distTotal = Genetico(provincias)


fp.realizarRecorrido(recorrido, distTotal)
print("FIN")
