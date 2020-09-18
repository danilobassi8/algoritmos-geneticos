import os
# para ocultar mensaje de bienvenida
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame.locals import *
import pygame
import curses
import parametros
import numpy as np
import math

# -------------- Traigo desde el script principal algunos parametros. ---------
long_estela = 94 * parametros.casilleros_estela
viento_maximo = parametros.vel_viento
param_dibujarMapaRugosidad = True

flags = DOUBLEBUF
tamaño_x = 800
tamaño_y = 800

# offsets
if(param_dibujarMapaRugosidad):
    offset_pantalla_x = 400 
else:
    offset_pantalla_x = 300
offset_pantalla_y = 0

screen = pygame.display.set_mode((tamaño_x + offset_pantalla_x, tamaño_y + offset_pantalla_y), flags)
vientoHaciaArriba = False
# creo grupos de sprites para despues cambiarlos.
molinos_sprites = pygame.sprite.Group()
viento_sprites = pygame.sprite.Group()


# Algunos colores.
WHITE = (255, 255, 255)
ORANGE = (255, 170, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SOFT_GREEN = (115, 219, 146)
ESTELA_C = (160, 224, 163)
POTENCIA_C = (218, 115, 187)
CELESTE = (36, 172, 242)

# carpeta de imagenes.
main_folder = os.path.dirname(__file__)
img_folder = os.path.join(main_folder, "img")


# declaro la fuente que voy a utilizar.
pygame.font.init()
myfont = pygame.font.SysFont('Arial Black', 12)
potfont = pygame.font.SysFont('Lucida Sans', 11)
confont = pygame.font.SysFont('Calibri', 17)
confontNegrita = pygame.font.SysFont('Calibri', 17)
confontNegrita.set_bold(True)

# creo una pantalla con cierto tamaño y despues la lleno de verde
screen.fill(SOFT_GREEN)
# le pongo titulo a la pantalla.
pygame.display.set_caption('Aerogeneradores - Algoritmos Genéticos - Grupo 3')


# dada una matriz, dibuja los cuadros de la imagen.
def dibujaCuadros(matriz):
    global tamaño_x, screen
    molinos = []

    # coloco los molinos.
    for fila in range(10):
        for columna in range(10):
            # posicion en pantalla
            posx = tamaño_x / 10 * columna
            posy = tamaño_y / 10 * fila

            if(matriz[fila][columna].HayGenerador):
                molino = Molino(posx, posy, matriz[fila][columna])
                molinos_sprites.add(molino)
                molinos.append(molino)

    for molino in molinos:

        casillerosOcupados = parametros.casilleros_estela

        # posicion en pantalla
        posx = molino.rect.center[0]
        posy = molino.rect.center[1]

        fila = int(posy / (tamaño_x / 10))
        columna = int(posx / (tamaño_x / 10))

        # recorro los casilleros ocupados por la estela y les dibujo un cuadrado de otro color + viento.
        for i in range(casillerosOcupados):
            pos = i + 1
            posActual = (fila - pos) if vientoHaciaArriba else (fila + pos)

            if(0 <= posActual <= 9):
                if(matriz[posActual][columna].HayGenerador):
                    molinoEstela = [m for m in molinos if m.rect.center == (posx, tamaño_y / 10 * (posActual))][0]
                    molinoEstela.colorFondo = ESTELA_C
                else:
                    rectangulo = pygame.Rect(posx, tamaño_y / 10 * (posActual), tamaño_x / 10, tamaño_x / 10)
                    pygame.draw.rect(screen, ESTELA_C, rectangulo)

                    # creo el efecto de viento
                    c = int(posx / (tamaño_x / 10))
                    f = int(posActual)
                    viento = Viento(posx, tamaño_y / 10 * (posActual), str(matriz[f][c].viento) + " m/s")
                    viento_sprites.add(viento)

    # dibuja las lineas verticales que marcan separacion de terreno.
    for i in range(11):
        pygame.draw.line(screen, BLACK, (0, tamaño_y / 10 * i), (tamaño_x, tamaño_y / 10 * i), 1)
        pygame.draw.line(screen, BLACK, (tamaño_x / 10 * i, 0), (tamaño_y / 10 * i, tamaño_y), 1)

    # dibujo una "segunda consola" a la derecha de la pantalla (offset)
    rectangulo = pygame.Rect((tamaño_x, 0), (offset_pantalla_x, tamaño_y + offset_pantalla_y))
    pygame.draw.rect(screen, BLACK, rectangulo)

    # muestra datos relevantes en la "segunda consola".
    textos = []
    c = matriz[0][0]
    textos.append("Generador:")
    textos.append(c.generador.nombre)

    textos.append("Tamaño del casillero (4.r): ")
    textos.append(str(c.generador.radio * 4) + " mts")
    textos.append("Tamaño del terreno: ")
    textos.append(str(c.generador.radio * 4 * 25) + " mts\N{SUPERSCRIPT TWO}")
    textos.append(" ")
    textos.append(" ")

    # calculo la potencia total generada por los molinos existentes.
    pot = 0
    cantGen = 0
    for f in range(10):
        for c in range(10):
            if(matriz[f][c].HayGenerador):
                cantGen += 1
                pot += matriz[f][c].generador.potenciaGenerada(matriz[f][c].viento)

    textos.append("Cantidad de turbinas: " + str(cantGen))
    textos.append("")
    textos.append("Potencia total generada: ")
    textos.append('{:,} kW'.format(pot))
    textos.append("Velocidad del viento:")
    textos.append(str(parametros.vel_viento) + " m/s - Constante -  ↓↓↓")
    textos.append("")

    if(param_dibujarMapaRugosidad):
        textos.append("")
        textos.append("Mapa de rugosidad")

    # recorro todos los textos que agregue y los muestro.
    for i in range(len(textos)):
        if(i % 2 == 1):
            text = confont.render(textos[i], False, WHITE)
            screen.blit(text, (tamaño_x + 20, 25 * i + 25))
        else:
            text = confontNegrita.render(textos[i], False, WHITE)
            screen.blit(text, (tamaño_x + 10, 25 * i + 25))

    DibujaMapaRugosidad(matriz)


def DibujaMapaRugosidad(matriz):
    if(param_dibujarMapaRugosidad):
        # Dibuja el mapa de rugosidad.
        for f in range(10):
            for c in range(10):
                rugosidad = matriz[f][c].z0

                rectangulo = pygame.Rect(tamaño_x + 107 + 21 * c, 450 + 21 * f, 20, 20)
                pygame.draw.rect(screen, colorPorZ(matriz[f][c].z0), rectangulo)

        # dibuja la escala.
        c = 0
        for z in np.arange(0, 0.1, 0.0005):
            c += 1
            rectangulo = pygame.Rect(tamaño_x + 110 + 1 * c, 680, 1, 10)
            pygame.draw.rect(screen, colorPorZ(z), rectangulo)

        escala_ini = confont.render('0', False, WHITE)
        escala_fin = confont.render('0.1', False, WHITE)
        screen.blit(escala_ini, (tamaño_x + 105, 700))
        screen.blit(escala_fin, (tamaño_x + 300, 700))


def colorPorZ(z):
    p_color = 10
    # escala de colores logaritmica.
    zt = 1.44 * math.log(z * p_color + 1)

    r = int(zt * 255)
    g = 255 - int(zt * 255)
    b = int(zt * 77)

    if(z < 0):
        return colorPorZ(0)
    if(z > 0.1):
        return colorPorZ(0.1)
    return (r, g, b)


# ------------------------------------------ CLASES ---------------------------------------- #


class Viento(pygame.sprite.Sprite):
    def __init__(self, x, y, viento):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_folder, "estela_0.png"))
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.colorFondo = ESTELA_C
        self.viento = viento

        # cargo todas las imagenes que voy a usar y las reescalo.
        self.frames = []
        for i in range(7):
            img_disco = pygame.image.load(os.path.join(img_folder, "estela_" + str(i) + ".png"))
            img = pygame.transform.scale(img_disco, (80, 80))
            self.frames.append(img)

    def update(self):
        # reproduzco el efecto del viento solo si el viento está perturbado.
        if(self.viento != str(viento_maximo) + " m/s"):
            # segun como viene el viento reproduzco de atras para adelante o adelante para atrás.
            if(self.viento != viento_maximo):
                if(vientoHaciaArriba):
                    self.frame += 1
                    if(self.frame > 6):
                        self.frame = 0
                else:
                    self.frame -= 1
                    if(self.frame < 0):
                        self.frame = 6

                rectangulo = pygame.Rect((self.rect.center[0] + 1, self.rect.center[1] + 1), (tamaño_x / 10 - 1, tamaño_x / 10 - 1))
                pygame.draw.rect(screen, self.colorFondo, rectangulo)

                screen.blit(self.frames[self.frame], self.rect.center)

                # dibuja la velocidad del viento.
                # textsurface = myfont.render(self.viento, False, BLACK)
                # screen.blit(textsurface, (self.rect.center[0] + 3, self.rect.center[1]))
        else:
            rectangulo = pygame.Rect((self.rect.center[0] + 1, self.rect.center[1] + 1), (tamaño_x / 10 - 1, tamaño_x / 10 - 1))
            pygame.draw.rect(screen, SOFT_GREEN, rectangulo)


class Molino(pygame.sprite.Sprite):
    def __init__(self, x, y, casillero):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "molino_0.png"))
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.colorFondo = SOFT_GREEN
        self.viento = str(casillero.viento) + " m/s"
        self.potenciaGenerada = str(casillero.generador.potenciaGenerada(casillero.viento)) + " kW"

        # cargo todas las imagenes que voy a usar y las reescalo.
        self.frames = []
        for i in range(7):
            img_disco = pygame.image.load(os.path.join(img_folder, "molino_" + str(i) + ".png"))
            img = pygame.transform.scale(img_disco, (80, 80))
            self.frames.append(img)

    def update(self):

        # solo paso de frame (giro el rotor) si el molino genera energia.
        if(self.potenciaGenerada != "0 kW"):
            self.frame += 1
            if(self.frame > 6):
                self.frame = 0
        else:
            self.frame = 3

        rectangulo = pygame.Rect((self.rect.center[0] + 1, self.rect.center[1] + 1), (tamaño_x / 10 - 1, tamaño_x / 10 - 1))
        pygame.draw.rect(screen, self.colorFondo, rectangulo)

        screen.blit(self.frames[self.frame], (self.rect.center[0], self.rect.center[1] + 5))

        # dibuja la velocidad del viento.
        textsurface = myfont.render(self.viento, False, BLACK)
        screen.blit(textsurface, (self.rect.center[0] + 3, self.rect.center[1]))

        # aca va a ir la potencia generada.
        rectangulo = pygame.Rect((self.rect.center[0], self.rect.center[1] + 67), (80, 14))
        pygame.draw.rect(screen, BLACK, rectangulo)

        textsurface = potfont.render("+" + self.potenciaGenerada, False, ORANGE)
        screen.blit(textsurface, (self.rect.center[0] + 12, self.rect.center[1] + 65))
