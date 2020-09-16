import os
import dbase as modelos
import parametros as params
import casillero as game
import math
import random
import genetico
import statistics
import matplotlib.pyplot as plt


class Casillero():
    generador = None

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.viento = 0
        self.HayGenerador = False
        self.bin = 1 if self.HayGenerador else 0
        self.potenciaGenerada = 0
        self.z0 = params.z0


def ejecutaViento(m):
    global casilleros_estela, c_induccion, c_arrastre, radio_estela
    # recorro los renglones de a una columna a la vez para ver como avanza el viento cada vez que se encuentra con una columna.
    v0 = params.vel_viento

    for fil in range(10):
        for col in range(10):
            casillero = m[fil][col]
            # si no fue asignado todavía
            if(casillero.viento == 0):
                casillero.viento = v0
                if(casillero.HayGenerador):
                    # ocupo los casilleros de abajo con el viento correspondiente.
                    propagaVientoHaciaAbajo(m, casillero, fil, col, v0)
            else:
                # si ya está asignado el valor pero hay molino (y esta prendido), propago.
                if(casillero.HayGenerador and casillero.generador.potenciaGenerada(casillero.viento) != 0):
                    propagaVientoHaciaAbajo(m, casillero, fil, col, casillero.viento)


def propagaVientoHaciaAbajo(m, casillero, fil, col, viento):

    # traigo los parametros necesarios.
    casilleros_estela = params.casilleros_estela
    const_prop_r_estela = params.const_prop_r_estela
    c_induccion = params.c_induccion
    v0 = viento

    for i in range(1, casilleros_estela + 1):
        pos_fila = fil + i

        if(0 <= pos_fila <= 9):
            if(m[pos_fila][col].HayGenerador == False):
                # asigno algo como para que ya quede que asigné
                m[pos_fila][col].viento = 1
            else:
                # calculo viento.
                # cociente
                coc = 2 * c_induccion
                # denominador.python
                gen = m[pos_fila][col].generador
                alfa = 1 / (2 * math.log(gen.altura / m[pos_fila][col].z0))
                x = 4 * gen.radio * i
                r1 = gen.radio * const_prop_r_estela
                den = (1 + alfa * (x / r1))**2
                # viento final.
                vFinal = v0 * (1 - coc / den)

                m[pos_fila][col].viento = round(vFinal, 2)
                break


def rellenarPoblacionInicial(cantCromosomas):
    poblacion = []

    for i in range(cantCromosomas):
        # creo una matriz y la relleno de casilleros en blanco.
        matriz = []
        for fila in range(10):
            renglon = []
            for columna in range(10):
                renglon.append(Casillero(fila, columna))
            matriz.append(renglon)

        # RELLENAR
        # ¿Generar menos de 25 generadores?

        cantMolinos = 0
        while cantMolinos < 25:
            numero1 = int(random.uniform(0, 10))
            numero2 = int(random.uniform(0, 10))
            casillero = matriz[numero1][numero2]
            if casillero.HayGenerador == False:
                casillero.HayGenerador = True
                cantMolinos += 1

        poblacion.append(matriz)

    return poblacion


def mostrarMolinos(matriz):
    for fila in range(10):
        print("")
        for columna in range(10):
            if(matriz[fila][columna].HayGenerador):
                print("[ X ]", end="")
            else:
                print("[   ]", end="")


def mostrarPotencias(matriz):
    for fila in range(10):
        print("")
        for columna in range(10):
            if(matriz[fila][columna].HayGenerador):
                n = matriz[fila][columna].potenciaGenerada
                print("  " + "{:.2f}".format(n).ljust(6) + " ", end="")
            else:
                n = 0
                print("  " + "{:.2f}".format(n).ljust(6) + " ", end="")


def mostrarVientos(matriz):
    for fila in range(10):
        print("")
        for columna in range(10):
            n = round(matriz[fila][columna].viento + 0.0, 2)
            print("  " + "{:.2f}".format(n).ljust(5) + " ", end="")
    print()
    print("----------------------------------")


def rellenarFuncionesObjetivoYFitness(poblacion):
    listaFObjetivo = []
    listaFitness = []

    # calcula listaFObjetivo
    for cromosoma in poblacion:
        ejecutaViento(cromosoma)
        fObjetivo = 0
        for fila in cromosoma:
            for casillero in fila:
                casillero.potenciaGenerada = casillero.generador.potenciaGenerada(casillero.viento)
                fObjetivo += casillero.potenciaGenerada
        listaFObjetivo.append(fObjetivo)

    # calcula el fitness
    sumatotal = sum(listaFObjetivo)
    for i in range(len(poblacion)):
        listaFitness.append(listaFObjetivo[i] / sumatotal)

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


def crossover(padres, prob):

    # hacer que se "purgen" los cruzados

    
    r = random.uniform(0, 1)
    p1 = padres[0].copy()
    p2 = padres[1].copy()

    hijo1 = []
    hijo2 = []

    if(prob <= prob):

        # primer hijo sale por mejores filas.

        for f in range(10):
            puntajeFila1 = 0
            puntajeFila2 = 0
            for c in range(10):
                if(p1[f][c].HayGenerador):
                    puntajeFila1 += p1[f][c].potenciaGenerada
                if(p2[f][c].HayGenerador):
                    puntajeFila2 += p2[f][c].potenciaGenerada
            if(puntajeFila1 >= puntajeFila2):
                hijo1.append(p1[f])
            else:
                hijo1.append(p2[f])

        # segundo hijo sale por mejores columnas

        for i in range(10):
            renglon = []
            for j in range(10):
                renglon.append(-1)
            hijo2.append(renglon)

        for c in range(10):
            puntajeColumna1 = 0
            puntajeColumna2 = 0
            for f in range(10):
                if(p1[f][c].HayGenerador):
                    puntajeColumna1 += p1[f][c].potenciaGenerada
                if(p2[f][c].HayGenerador):
                    puntajeColumna2 += p2[f][c].potenciaGenerada
            if (puntajeColumna1 >= puntajeColumna2):
                for f in range(10):
                    hijo2[f][c] = p1[f][c]
            else:
                for f in range(10):
                    hijo2[f][c] = p2[f][c]
    else:
        hijo1 = p1.copy()
        hijo2 = p2.copy()

    return hijo1, hijo2


def mutacion(hijoOriginal, prob):
    # hacemos una copia para que no ocurran problemas de referencias de Python
    hijo = hijoOriginal.copy()
    r = random.uniform(0, 1)

    # Inversion mutation con toda una fila elegida al azar.
    if(r <= prob):
        numero = int(random.uniform(0, len(hijo)))
        fila = hijo[numero]
        for i in range(int(len(fila) / 2)):
            aux = fila[len(fila) - i - 1]
            fila[len(fila) - i - 1] = fila[i]
            fila[i] = aux

    return hijo


def elitismo(poblacion, listaFitness, cantElite):
    # Creamos una copia de la lista (Fitness u objetivo), elegimos el mejor, lo borramos
    # y volvemos a elegir el mejor. Luego sacamos los indices en el arreglo original.
    # y agregamos en la proximaGeneracion la poblacion en el indice de los mejores.
    indiceMejor = []
    copiaFitness = listaFitness.copy()
    elites = []

    for i in range(cantElite):
        mejor = max(copiaFitness)
        indiceMejor.append(listaFitness.index(mejor))
        copiaFitness.remove(mejor)

    for i in range(cantElite):
        elites.append(poblacion[indiceMejor[i]])

    return elites


def mostrarGraficasEnPantalla(ejeX, minimos, maximos, media, minHistorico):
    plt.plot(ejeX, minimos, label='Minimos', linewidth=4, color="red", alpha=0.6)
    plt.plot(ejeX, maximos, label='Maximos', linewidth=4, color="blue", alpha=0.6)
    plt.plot(ejeX, media, label='Media', linewidth=4, color="green", alpha=0.6)
    plt.plot(ejeX, minHistorico, label='Mejor Historico', linewidth=4, color="purple", alpha=0.2)

    plt.legend()
    plt.ylabel(' Valor de la Funcion Objetivo ')
    plt.xlabel(' Generación ')
    plt.show()


def Algoritmo_Genetico(generador):
    Casillero.generador = generador

    # ------------------- Definiciones de variables ------------------- #

    # arreglos para las graficas.
    mostrarGraficas = True  # si no se quieren mostrar graficas de rendimiento poner en false.
    ejeX = []
    minimos = []
    maximos = []
    medias = []
    mejorHistorico = []

    # Poblacion
    poblacion = []
    proximaGeneracion = []

    # Lista F objetivo y F Fitness.
    listaFObjetivo = []
    listaFitness = []

    # Parametros.
    cantMaximaGeneraciones = 200
    # probabilidades
    p_crossover = 0.9
    p_mutacion = 0.05
    cantIndividuosEnPoblacion = 50

    # mejores temporales
    mejorCromosoma = 0
    mejorPuntaje = 0

    # ------------------- Comienzo del programa ------------------- #

    hayElitismo = input("¿Aplicar elitismo? (s/n): ")
    if(hayElitismo.lower() == 's'):
        hayElitismo = True
        cantElite = 2
    else:
        hayElitismo = False
        cantElite = 0

    poblacion = rellenarPoblacionInicial(cantIndividuosEnPoblacion)
    listaFitness, listaFObjetivo = rellenarFuncionesObjetivoYFitness(poblacion)

    cantidadCiclos = 0
    terminado = False
    while (terminado == False):
        cantidadCiclos = cantidadCiclos + 1
        print("GENERACIÓN ", cantidadCiclos, " LISTA.")

        if(hayElitismo):
            elites = elitismo(poblacion,listaFitness,cantElite)
            
            for e in elites:
                proximaGeneracion.append(e)

        for i in range(int((len(poblacion) - cantElite) / 2)):

            # seleccionar 2 individuos para el cruce
            padres = seleccionarPareja(poblacion, listaFitness)
            # cruzar con cierta probabilidad 2 individuos y obtener descendientes
            hijos = crossover(padres, p_crossover)
            
            # hacer que se "purgen" los cruzados
            
            # Mutar con cierta probabilidad
            hijomutado1 = mutacion(hijos[0], p_mutacion)
            hijomutado2 = mutacion(hijos[1], p_mutacion)
            # Insertar descendientes en la proxima generacion
            proximaGeneracion.append(hijomutado1)
            proximaGeneracion.append(hijomutado2)

        poblacion = proximaGeneracion.copy()
        proximaGeneracion = []
        listaFObjetivo = []
        listaFitness = []
        # rellena funcion fitness y objetivo.
        listaFitness, listaFObjetivo = rellenarFuncionesObjetivoYFitness(poblacion)

        # Guarda el mejor cromosoma
        maximoActual = max(listaFObjetivo)
        indice_maximo = listaFObjetivo.index(maximoActual)
        if (mejorPuntaje < maximoActual):
            mejorCromosoma = poblacion[indice_maximo]
            mejorPuntaje = maximoActual

        # GRAFICOS
        ejeX.append(cantidadCiclos)
        minimos.append(min(listaFObjetivo))
        maximos.append(max(listaFObjetivo))
        medias.append(statistics.mean(listaFObjetivo))
        mejorHistorico.append(mejorPuntaje)

        if(cantidadCiclos == cantMaximaGeneraciones):
            terminado = True

    # plotea las graficas.
    mostrarGraficasEnPantalla(ejeX, minimos, maximos, medias, mejorHistorico)
    return mejorCromosoma
