# defino algunos colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
tamaño_circulo = 6
# ---
provincias = []
provinciaSeleccionada = ''


def DibujaCirculo(p, screen, color):
    import pygame
    # declaro la fuente de texto que voy a usar
    pygame.font.init()
    myfont = pygame.font.SysFont('Calibri', 14)
    # dibuja un circulo en una posicion x y
    global tamaño_circulo
    pygame.draw.circle(screen, color, (p[1], p[2]), tamaño_circulo)

    # para que imprima el texto de la provincia.
    textsurface = myfont.render(p[0], False, RED)
    screen.blit(textsurface, (p[1] + 10, p[2] - 10))


def inicializarPantalla():
    import os
    import pygame
    import datos
    provincias = datos.provincias

    # inicializo el juego.
    pygame.init()
    # creo una pantalla con cierto tamaño y despues la lleno de negro.
    tamaño_x = 850
    tamaño_y = 1000
    screen = pygame.display.set_mode((tamaño_x, tamaño_y))
    screen.fill((255, 255, 255))
    # le pongo titulo a la pantalla.
    pygame.display.set_caption('Problema del viajante.')
    # fuente de texto
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 30)
    # cargo la imagen en la variable mapa.

    dir_file = os.path.dirname(os.path.abspath(__file__))
    dir_img = dir_file + "\\arg.png"
    mapa = pygame.image.load(r"{}".format(dir_img))

    # hago que la imagen se ajuste a el tamaño de pantalla.
    mapa = pygame.transform.scale(mapa, (tamaño_x, tamaño_y))
    screen.blit(mapa, (0, 0))
    # dibujo circulos para cada provincia.
    for p in provincias:
        DibujaCirculo(p, screen, BLACK)
    pygame.display.update()
    return pygame, screen


def elegirProvincia():
    import os
    import pygame
    import datos
    provincias = datos.provincias

    pygame, screen = inicializarPantalla()

    os.system('cls')
    print(' Elija la provincia inicial')

    encontroProv = False
    while encontroProv == False:
        for event in pygame.event.get():
            # para el boton de salir
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = pygame.mouse.get_pos()
                # verifico si clickeo algun circulo.
                for p in provincias:
                    if(clicked[0] <= p[1] + tamaño_circulo and clicked[0] >= p[1] - tamaño_circulo):
                        if(clicked[1] <= p[2] + tamaño_circulo and clicked[1] >= p[2] - tamaño_circulo):
                            provinciaSeleccionada = p
                            encontroProv = True
    pygame.quit()
    return provinciaSeleccionada


def realizarRecorrido(recorrido, dist):
    import os
    import pygame
    import datos
    from time import sleep

    pygame, screen = inicializarPantalla()
    provincias = datos.provincias

    # declaro la fuente de texto.
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 30)

    for i in range(len(recorrido) - 1):
        # dibujo una linea desde la provincia i hasta la i+1.
        p1 = recorrido[i]
        p2 = recorrido[i + 1]
        pygame.draw.line(screen, BLUE, (p1[1], p1[2]), (p2[1], p2[2]), 3)
        pygame.display.update()
        sleep(0.1)

    # renderizo el aviso de fin.
    # renderizo un rectangulo de fondo.
    rect = pygame.Rect(0, 0, 850, 40)
    pygame.draw.rect(screen, BLACK, rect)
    # renderizo texto
    textsurface = myfont.render('   ' + str(dist) + ' kilometros recorridos', False, RED)
    screen.blit(textsurface, (0, 2))
    pygame.display.update()

    # doy el listado de como se recorrieron las provincias en consola.
    os.system("cls")
    print(" Las capitales se recorrieron en este orden:")
    for p in recorrido:
        print(' - ' + p[0])
    print()
    print(" Cantidad de Km recorridos: " + str(dist))

    while True:
        for event in pygame.event.get():
            # presiona tecla para salir
            if event.type == pygame.KEYDOWN:
                return
        if event.type == pygame.QUIT:
            return
