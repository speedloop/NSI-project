import pygame 



def test_collide_play(mouse_pos,playrect):
    if playrect.collidepoint(mouse_pos):
        print("ca collide")
        return True
    return False

pygame.font.init()

ecran = pygame.display.set_mode((1300,900))
ecran.fill((80,80,80))

font = pygame.font.Font("blantic.otf",48)
play = font.render("PLAY", 1,(250,250,0))
play_rect = pygame.rect.Rect((50,750,play.get_width(),play.get_height()))
ecran.blit(play,(50,750))

pygame.display.update()

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                continuer = False
                
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            ecran.fill((80,80,80))
            if test_collide_play(mouse_pos, play_rect):
                pygame.draw.rect(ecran,(255,128,0),(45,745,127,66))
            ecran.blit(play,(50,750))

    pygame.display.update()
            
pygame.quit()