import os
import pandas as pd
import math

provincias = [
    # Capital, x , y, posEnExcel
    ("Cdad. de Bs. As.", 514, 374, 0),
    ("Córdoba", 363, 285, 1),
    ("Corrientes", 517, 185, 2),
    ("Formosa", 529, 142, 3),
    ("La Plata", 530, 395, 4),
    ("La Rioja", 289, 234, 5),
    ("Mendoza", 241, 331, 6),
    ("Neuquén", 273, 494, 7),
    ("Paraná", 465, 300, 8),
    ("Posadas", 593, 179, 9),
    ("Rawson", 350, 610, 10),
    ("Resistencia", 503, 170, 11),
    ("Río Gallegos", 285, 844, 12),
    ("S.F.d.V.d. Catamarca", 317, 206, 13),
    ("S.M. de Tucumán", 331, 163, 14),
    ("S.S. de Jujuy", 326, 88, 15),
    ("Salta", 324, 104, 16),
    ("San Juan", 246, 292, 17),
    ("San Luis", 307, 338, 18),
    ("Santa Fe", 455, 285, 19),
    ("Santa Rosa", 365, 427, 20),
    ("Sgo. Del Estero", 359, 185, 21),
    ("Ushuaia", 308, 927, 22),
    ("Viedma", 404, 545, 23),
]

# leo los datos del excel y los meto en la variable datos
dir_file = os.path.dirname(os.path.abspath(__file__))
dir_db = dir_file + "\TablaCapitales.xlsx"
datos = pd.read_excel(r"{}".format(dir_db))



# los datos se pueden llamar de la forma: data[0][0]
# o con el nombre del renglón data['Córdoba'][0]


def CalculaDistancia(provA, provB):
    global datos
    return datos[provA[0]][provB[3]]


def CalculaProvMinDistancia(provA, arrayRepetidos):
    global datos
    prov = provA[0]

    provinciaMasCercana = ''
    distMin = math.inf

    # busco entre todas las distancias la mas corta.
    for p in provincias:
        dist = datos[prov][p[3]]
        if(0 < dist < distMin):
            if(p not in arrayRepetidos):
                provinciaMasCercana = p
                distMin = dist

    # devuelvo la provincia mas cercana y la distancia.
    return provinciaMasCercana, distMin

def mapearRecorrido(recorridoNumerico):
    recorrido = []
    for n in recorridoNumerico:
        recorrido.append(provincias[n])
    return recorrido

def CalculaDistanciaDeRecorrido(r):
    global datos

    # antes de nada, hago que a la distancia del recorrido se le sume la vuelta.
    recorridoNumerico = r + [r[0]]

    distTotal = 0
    # tengo que "mapear" el recorrido, porque lo recibí en numeros.
    recorrido = mapearRecorrido(recorridoNumerico)

    for i in range(len(recorrido) - 1):
        pActual = recorrido[i]
        pProx = recorrido[i + 1]
        dist = datos[pActual[0]][pProx[3]]
        distTotal += dist
    return distTotal
