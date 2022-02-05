import pygame

def settings(screen):
    screen.fill((80,80,80))
    pygame.display.update()

    continuer = True
    while(continuer):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True