import os
import dbase as modelos
import parametros as params
import casillero as game
import math
import random
import genetico
os.system("cls")


# ------------------------------------------------------------------------------------------------------------------------------------------------------ #
# ---------------------------------------------------------------          MAIN          --------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------------ #

# elige el generador.
generador = modelos.ObtenerGenerador()
# uso el algoritmo genetico para traerme el mejor cromosoma.
mejorCromosoma =  genetico.Algoritmo_Genetico(generador)
# lo muestro en pantalla.
game.MostrarPantallaConMolinos(mejorCromosoma)
