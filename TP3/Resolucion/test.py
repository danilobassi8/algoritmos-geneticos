# TEST PARA EL CROSSOVER CICLICO.

def Crossover_Ciclico(p1, p2):
    # se copia para resolver problemas de referencias #
    hijo = p2.copy()
    indexP1 = 0
    sigue = True
    while(sigue):
        hijo[indexP1] = p1[indexP1]

        valorP2 = p2[indexP1]
        # actualizo el indice de 1
        indexP1 = p1.index(valorP2)

        if(valorP2 in hijo):
            sigue = False

    return hijo



p1 = [9,8,2,1,7,4,5,10,6,3]
p2 = [1,2,3,4,5,6,7,8,9,10]
print("PADRES")
print(p1)
print(p2)
print("HIJOS")
print(Crossover_Ciclico(p1,p2))
print(Crossover_Ciclico(p2,p1))