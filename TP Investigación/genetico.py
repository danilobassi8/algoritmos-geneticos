import os
import dbase as modelos
import parametros as params
import casillero as game
import math
import random
import statistics
import matplotlib.pyplot as plt
from copy import copy
from tqdm import tqdm


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
        self.vientoAsignado = False


def ejecutaViento(cromosoma):
    # traigo los parametros necesarios.
    casilleros_estela = params.casilleros_estela
    const_prop_r_estela = params.const_prop_r_estela
    c_induccion = params.c_induccion
    v0 = params.vel_viento
    m = cromosoma.copy()

    for c in range(10):
        fila_prop = -1
        for f in range(10):
            # fina en la que se propagó ultimo
            fila_prop += 1

            if(fila_prop >= f):
                casillero = m[f][c]
                if(casillero.vientoAsignado == False):
                    casillero.viento = v0

                if(casillero.HayGenerador):
                    # asignar la potencia.
                    casillero.potenciaGenerada = casillero.generador.potenciaGenerada(casillero.viento)

                    # propagar el viento (SI ESTÁ PRENDIDO).
                    if(casillero.generador.potenciaGenerada(casillero.viento) > 0):
                        for i in range(1, casilleros_estela + 1):
                            pos_fila = f + i
                            fila_prop += 1
                        # asigno siempre y cuando no me salga de la matriz de 10x10
                            if(0 <= pos_fila <= 9):
                                # calculo su viento.
                                # cociente
                                coc = 2 * c_induccion
                                # denominador
                                gen = m[pos_fila][c].generador
                                alfa = 1 / (2 * math.log(gen.altura / m[pos_fila][c].z0))
                                x = 4 * gen.radio * i
                                r1 = gen.radio * const_prop_r_estela
                                den = (1 + alfa * (x / r1))**2
                                # viento final.
                                vientoPadre = m[f][c].viento
                                vFinal = vientoPadre * (1 - coc / den)

                                # le actualizo el viento
                                m[pos_fila][c].viento = round(vFinal, 2)
                                m[pos_fila][c].vientoAsignado = True

                                # si tiene generador (Y ESTE ESTÁ PRENDIDO), tengo que parar porque ese propaga hacia abajo.
                                if(m[pos_fila][c].HayGenerador):
                                    if(m[pos_fila][c].generador.potenciaGenerada(m[pos_fila][c].viento) > 0):
                                        break

            # si ya le asigne el viento, no hago nada
            # recorro los renglones de a una columna a la vez para ver como avanza el viento cada vez que se encuentra con una columna.

    # una vez terminado, vuelvo a poner vientoAsignado en false.
    for f in range(10):
        for c in range(10):
            m[f][c].vientoAsignado = False
            # me aseguro de que si no tiene generador, no genera nada.
            if(m[f][c].HayGenerador == False):
                m[f][c].potenciaGenerada = 0

    return m


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
    print("molinos")
    for fila in range(10):
        print("")
        for columna in range(10):
            if(matriz[fila][columna].HayGenerador):
                print("[ X ]", end="")
            else:
                print("[   ]", end="")
    print()


def mostrarPotencias(matriz):
    print("potencias")
    for fila in range(10):
        print("")
        for columna in range(10):
            n = matriz[fila][columna].potenciaGenerada
            print("  " + "{:.2f}".format(n).ljust(6) + " ", end="")
    print()


def mostrarVientos(matriz):
    print("vientos:")
    for fila in range(10):
        print("")
        for columna in range(10):
            n = round(matriz[fila][columna].viento + 0.0, 2)
            print("  " + "{:.2f}".format(n).ljust(5) + " ", end="")
    print()


def rellenarFuncionesObjetivoYFitness(poblacion):
    listaFObjetivo = []
    listaFitness = []

    # calcula listaFObjetivo
    for cromosoma in poblacion:
        cromosoma = ejecutaViento(cromosoma)

        fObjetivo = 0
        for fila in cromosoma:
            for casillero in fila:
                if(casillero.HayGenerador):
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

        # creo un cromosoma nuevo que es la copia de la poblacion[indice]
        cromoNuevo = []
        for f in range(10):
            renglon = []
            for c in range(10):
                casillero = copy(poblacion[indice][f][c])
                renglon.append(casillero)
            cromoNuevo.append(renglon)
        # lo agrego a la pareja a devolver.
        pareja.append(cromoNuevo)

    return pareja


def crossover(padres, prob):
    r = random.uniform(0, 1)

    p1 = padres[0]
    p2 = padres[1]

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

        # vuelvo a ejecutar el viento
        hijo1 = ejecutaViento(hijo1)
        hijo2 = ejecutaViento(hijo2)

        # los purgo
        hijo1 = purgar(hijo1)
        hijo2 = purgar(hijo2)
    else:
        hijo1 = p1
        hijo2 = p2

    return hijo1, hijo2


def purgar(m):
    matriz = m
    aerogeneradores = []
    for f in range(10):
        for c in range(10):
            if(matriz[f][c].HayGenerador):
                aerogeneradores.append(matriz[f][c])

    # ordeno la lista por potencia generada de menor a mayor y me quedo solo con los 25 mejores
    aerogeneradores.sort(key=lambda x: x.potenciaGenerada, reverse=False)
    while(len(aerogeneradores) > 25):
        a = aerogeneradores[0]
        matriz[a.fila][a.columna].HayGenerador = False
        aerogeneradores.remove(aerogeneradores[0])

    # creo una copia del cromosoma con esos 25 mejores.
    cromo = []
    for f in range(10):
        renglon = []
        for c in range(10):
            renglon.append(Casillero(f, c))
        cromo.append(renglon)

    for a in aerogeneradores:
        cromo[a.fila][a.columna].HayGenerador = True
    cromo = ejecutaViento(cromo)

    return cromo


def mutacion(hijo, prob):
    # Inversion mutation con toda una fila elegida al azar.
    r = random.uniform(0, 1)
    if(r <= prob):
        # saco el numero de la fila
        numero = round(random.uniform(0, 9))
        fila = hijo[numero]

        # genero dos posiciones aleatorias
        pos1 = round(random.uniform(0, 9))
        pos2 = round(random.uniform(0, 9))
        # determino cual es el maximo y cual el minimo
        pos1, pos2 = min([pos1, pos2]), max([pos1, pos2])
        pos2c = pos2

        # creo una nueva fila vacia de diez lugares
        filaNueva = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # hasta pos1 son copio la fila original en la fila vacia
        for i in range(pos1):
            filaNueva[i] = fila[i]
        # desde pos1 a pos2 son intercambio
        while (pos1 <= pos2):
            filaNueva[pos1] = fila[pos2]
            filaNueva[pos2] = fila[pos1]
            pos1 += 1
            pos2 -= 1
        # desde pos2 al final copio la fila original
        for i in range(1,10-pos2c):
            filaNueva[pos2c + i] = fila[pos2c + i]
        # cambio la fila por la filanueva
        hijo[numero] = filaNueva
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
    plt.plot(ejeX, minimos, label='Minimos', linewidth=4, color="blue", alpha=0.6)
    plt.plot(ejeX, maximos, label='Maximos', linewidth=4, color="red", alpha=0.6)
    plt.plot(ejeX, media, label='Media', linewidth=4, color="green", alpha=0.6)
    plt.plot(ejeX, minHistorico, label='Mejor Historico', linewidth=4, color="purple", alpha=0.2)

    plt.legend()
    plt.ylabel(' Valor de la Funcion Objetivo ')
    plt.xlabel(' Generación ')

    # guarda la foto y la muestra
    directorio = os.path.dirname(os.path.abspath("main.py"))
    plt.savefig(directorio + '/img/ultimaCorrida.png')
    


def Algoritmo_Genetico(generador):
    Casillero.generador = generador
    # ------------------- Definiciones de variables ------------------- #

    # arreglos para las graficas.
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
    p_mutacion = 0.2
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
    print()

    poblacion = rellenarPoblacionInicial(cantIndividuosEnPoblacion)
    listaFitness, listaFObjetivo = rellenarFuncionesObjetivoYFitness(poblacion)

    cantidadCiclos = 0

    # esta linea es para que se muestre una barra de carga con ciertas opciones
    with tqdm(total=cantMaximaGeneraciones, ncols=60,
              bar_format="{desc}: >{percentage:.0f}%|{bar}| Generación: {n_fmt}/{total_fmt}") as barra:

        for cantidadCiclos in range(cantMaximaGeneraciones):
            barra.update()

            if(hayElitismo):
                elites = elitismo(poblacion, listaFitness, cantElite)

                for e in elites:
                    proximaGeneracion.append(e)

            for i in range(int((len(poblacion) - cantElite) / 2)):

                # seleccionar 2 individuos para el cruce
                padres = seleccionarPareja(poblacion, listaFitness)

                # cruzar con cierta probabilidad 2 individuos y obtener descendientes
                hijo1, hijo2 = crossover(padres, p_crossover)

                # Mutar con cierta probabilidad
                hijomutado1 = mutacion(hijo1, p_mutacion)
                hijomutado2 = mutacion(hijo2, p_mutacion)

                # Insertar descendientes en la proxima generacion
                proximaGeneracion.append(hijomutado1)
                proximaGeneracion.append(hijomutado2)

            poblacion = (proximaGeneracion).copy()

            proximaGeneracion = []
            listaFObjetivo = []
            listaFitness = []

            # rellena funcion fitness y objetivo.
            listaFitness, listaFObjetivo = rellenarFuncionesObjetivoYFitness(poblacion)

            indiceMaximo = listaFObjetivo.index(max(listaFObjetivo))
            cromo_maximo_actual = poblacion[indiceMaximo]
            if(mejorPuntaje <= max(listaFObjetivo)):
                mejorPuntaje = max(listaFObjetivo)
                mejorCromosoma = cromo_maximo_actual.copy()

            # GRAFICOS
            ejeX.append(cantidadCiclos)
            minimos.append(min(listaFObjetivo))
            maximos.append(max(listaFObjetivo))
            medias.append(statistics.mean(listaFObjetivo))
            mejorHistorico.append(mejorPuntaje)

    # una vez terminado el algoritmo genetico
    os.system("cls")
    print("-------------------------------------")

    mostrarMolinos(mejorCromosoma)
    mostrarVientos(mejorCromosoma)

    print("Potencia total generada: " + str(mejorPuntaje))
    print("-------------------------------------")

    # plotea las graficas
    mostrarGraficasEnPantalla(ejeX, minimos, maximos, medias, mejorHistorico)

    return mejorCromosoma
