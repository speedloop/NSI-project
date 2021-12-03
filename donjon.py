import pygame 

ecran = pygame.display.set_mode((640,480))

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
            
pygame.quit()