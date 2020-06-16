import os

# volumen y peso se usan indistintamente porque cumplen la misma función.
class Objeto:
    def __init__(self, numero, volumen, precio):
        self.numero = numero
        self.valor = precio
        self.volumen = volumen
        self.proporcion = precio/volumen


class Mochila:
    # variable de clase.
    volumenMaximo = 0

    def __init__(self, numero):
        # variables de instancia.
        self.listaObjetos = []
        self.valor = 0
        self.volumenOcupado = 0
        self.factible = True
        self.binario = numero

    def agregarObjeto(self, objeto):
        self.listaObjetos.append(objeto)
        self.valor += objeto.valor
        self.volumenOcupado += objeto.volumen
        if (self.volumenOcupado > self.volumenMaximo):
            self.factible = False

    def mostrar(self):
        global parte

        print(" ----------------------- ")
        print()
        print("Mochila: " + str(self.binario))
        print()

        print("Contiene:")

        if(parte.lower() == 'a'):  # si se eligio la parte A.
            for obj in self.listaObjetos:
                print("    objeto: " + str(obj.numero) + " ---- Precio: " +
                      str(obj.valor) + "  Volumen:" + str(obj.volumen))
            print()
            print("Volumen total: " + str(self.volumenOcupado) +
                  " Precio Total: " + str(self.valor))
        else:  # si se eligio la parte B.
            for obj in self.listaObjetos:
                print("    objeto:" + str(obj.numero) + " ---- Precio: " +
                      str(obj.valor) + "  Peso:" + str(obj.volumen))
            print()
            print("Volumen total: " + str(self.volumenOcupado) +
                  " Peso Total: " + str(self.valor))
        print()
        print(" ----------------------- ")

    def mostrarInfoMinima(self):
        print(" ----- mochila: " + str(self.binario) +  " -----")

        print("{  ", end="")
        for obj in self.listaObjetos:
            print(str(obj.numero) + "  ", end="")
        print("}")
        print("Volumen total: " + str(self.volumenOcupado) +
              " Precio Total: " + str(self.valor))
        print()

# Obtiene el mejor objeto de la tabla que se mande por parametro.


def mejorObjetoDeTabla(tabla):
    maximo = 0
    mejorObjeto = 0
    for obj in tabla:
        if(obj.proporcion >= maximo):
            maximo = obj.proporcion
            mejorObjeto = obj
    return mejorObjeto


os.system("cls")
print(" ---------------------------------------------------- ")
print()
parte = input("¿Desea elegir la parte A o B? :")
print()
print(" ---------------------------------------------------- ")
os.system("cls")

# se elije que tabla y tamaño de mochila utilizar segun si se elije la parte A o B del enunciado.
if(parte.lower() == 'a'):
    tabla = [
        Objeto(1, 150, 20),
        Objeto(2, 325, 40),
        Objeto(3, 600, 50),
        Objeto(4, 805, 36),
        Objeto(5, 430, 25),
        Objeto(6, 1200, 64),
        Objeto(7, 770, 54),
        Objeto(8, 60, 18),
        Objeto(9, 930, 46),
        Objeto(10, 353, 28)
    ]
    # setea el volumen de la clase mochila.
    Mochila.volumenMaximo = 4200
else:
    tabla = [
        Objeto(1, 1800, 72),
        Objeto(2, 600, 36),
        Objeto(3, 1200, 60),
    ]
    # setea el "volumen" (peso maximo) de la clase mochila.
    Mochila.volumenMaximo = 3000


print(" ---------------------------------------------------- ")
print()
b = input("¿Desea resolverlo con Metodo Exhaustivo? (S/N): ")
print()
print(" ---------------------------------------------------- ")
os.system("cls")


if(b.lower() == 's'):  # se resuelve por metodo exhaustivo.
    mochilas_factibles = []
    mejorValor = 0
    mejorBinario = 0
   # Generación del numero binario
    for i in range(2**len(tabla)):
        
        # zfill rellena con ceros el numero para que sea de 10 digitos.
        numero = bin(i).replace("0b", "").zfill(len(tabla))

        mochila = Mochila(numero)
        for j in range(len(numero)):
            if(numero[j] == '1'):
                mochila.agregarObjeto(tabla[j])

        if(mochila.factible):  # evalua volumen
            # comentar esta linea si no es necesario guardar todas las mochilas factibles (no se utiliza).
            mochilas_factibles.append(mochila)
            if(mejorValor <= mochila.valor):
                mejorBinario = numero
                mejorValor = mochila.valor

    #regenero la mejor mochila.
    mejorMochila = Mochila(mejorBinario)
    for i in range(len(mejorBinario)):
        if(mejorBinario[i] == '1'):
            mejorMochila.agregarObjeto(tabla[i])
    mejorMochila.mostrar()

    rta = input("¿Desea mostrar la lista de mochilas factibles ordenadas por mejor precio? (S/N): ")
    if(rta.lower() == 's'):
        os.system("cls")
        #ordena el array de mochilas_factibles por su valor.
        mochilas_factibles.sort(key=lambda x: x.valor, reverse=True)

        #las muestra.
        for m in mochilas_factibles:
            m.mostrarInfoMinima()

else:  # se resuelve por el metodo Greedy.
    copiaTabla = tabla.copy()
    # la tabla se copia porque le vamos a ir eliminando sus objetos a medidas que se agreguen.

    mochila = Mochila("Metodo greedy")

    # mientras siga habiendo elementos en la copiaTabla.
    while(len(copiaTabla) > 0):
        objeto = mejorObjetoDeTabla(copiaTabla)
        if(mochila.volumenOcupado+objeto.volumen <= mochila.volumenMaximo):  # si entra
            mochila.agregarObjeto(objeto)
        copiaTabla.remove(objeto)

    mochila.mostrar()
