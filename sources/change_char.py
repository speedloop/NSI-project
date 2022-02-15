import pygame

def change_char(screen):
    screen.fill((0,0,255))
    pygame.display.update()

    continuer = True
    while continuer :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

