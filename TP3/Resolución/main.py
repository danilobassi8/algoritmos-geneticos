import funciones_pantalla as fp
import datos


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


# --------------------------- INICIO DEL ALGORITMO --------------------------- #
provinciaInicial = fp.elegirProvincia()
provincias = datos.provincias

recorrido, distTotal = greedy(provinciaInicial)

fp.realizarRecorrido(recorrido, distTotal)
print("FIN")