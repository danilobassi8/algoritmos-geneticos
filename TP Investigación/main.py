import os
import dbase as modelos
import parametros as params
import casillero as game
import math
import random
import genetico

os.system("cls")


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


def mostrarVientos(matriz):
    for fila in range(10):
        print("")
        for columna in range(10):
            n = round(matriz[fila][columna].viento + 0.0, 2)
            print("  " + "{:.2f}".format(n).ljust(5) + " ", end="")
    print()
    print("----------------------------------")


def mostrarMolinos(matriz):
    for fila in range(10):
        print("")
        for columna in range(10):
            if(matriz[fila][columna].HayGenerador):
                print("[ X ]", end="")
            else:
                print("[   ]", end="")




# ------------------------------------------------------------------------------------------------------------------------------------------------------ #
# ---------------------------------------------------------------          MAIN          --------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------------ #

# elige el generador
generador = modelos.ObtenerGenerador()
Casillero.generador = generador

genetico.Algoritmo_Genetico(generador)
