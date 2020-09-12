
#main loop
def MostrarPantallaConMolinos(matriz):
    import funciones_pantalla as fpantalla
    import pygame
    import os


    # llamo a las funciones necesarias para inicializar pantalla
    fpantalla.dibujaCuadros(matriz)
    pygame.init()
    clock = pygame.time.Clock()
    FPS = 20

    
    
    terminado = False
    while terminado == False:
        # eventos de sistema.
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminado = True
        
        # Actualizacion
        fpantalla.molinos_sprites.update()
        fpantalla.viento_sprites.update()
    pygame.quit