import os
import dbase as modelos
import parametros as params
import casillero as game
import math
import random
import genetico
import statistics
import matplotlib.pyplot as plt
import copy

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
def purgar(m):
    matriz = m

    aerogeneradores = []
    for f in range(10):
        for c in range(10):
            if(matriz[f][c].HayGenerador):
                aerogeneradores.append(matriz[f][c])

    aerogeneradores.sort(key=lambda x: x.potenciaGenerada, reverse=False)
    while(len(aerogeneradores)>25):
        a = aerogeneradores[0]
        matriz[a.fila][a.columna].HayGenerador = False
        aerogeneradores.remove(aerogeneradores[0])

    return matriz

# --------------------------------------------------------------------------------------------------------------------- #
generador = modelos.ObtenerGenerador()
Casillero.generador = generador

m = []
for f in range(10):
    renglon = []
    for c in range(10):
        casillero = Casillero(f,c)
        renglon.append(casillero)
    m.append(renglon)

m[0][1].HayGenerador = True
m[0][2].HayGenerador = True
m[0][3].HayGenerador = True
m[0][4].HayGenerador = True
m[0][5].HayGenerador = True
m[0][6].HayGenerador = True
m[0][9].HayGenerador = True
m[1][0].HayGenerador = True
m[1][7].HayGenerador = True
m[2][2].HayGenerador = True
m[2][5].HayGenerador = True
m[3][1].HayGenerador = True
m[3][4].HayGenerador = True
m[3][8].HayGenerador = True
m[3][9].HayGenerador = True
m[4][3].HayGenerador = True
m[5][5].HayGenerador = True
m[5][8].HayGenerador = True
m[5][9].HayGenerador = True
m[6][4].HayGenerador = True
m[6][6].HayGenerador = True
m[7][1].HayGenerador = True
m[7][2].HayGenerador = True
m[7][9].HayGenerador = True
m[7][7].HayGenerador = True
m[8][4].HayGenerador = True
m[8][6].HayGenerador = True
m[9][0].HayGenerador = True
m[9][1].HayGenerador = True
m[9][2].HayGenerador = True
m[9][3].HayGenerador = True
m[9][4].HayGenerador = True


m = ejecutaViento(m)

mostrarMolinos(m)
mostrarVientos(m)
mostrarPotencias(m)


m = purgar(m)
m = ejecutaViento(m)
print(" PURGADO ////////////////////////////////////////////////////////////////////// ")

mostrarMolinos(m)
mostrarVientos(m)
mostrarPotencias(m)



