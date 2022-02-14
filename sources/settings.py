import pygame
from sources.constantes import *

def settings(screen):
    screen.fill((80,80,80))    

    pygame.draw.rect(screen, (0,0,0),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),border_radius=15)
    pygame.draw.rect(screen, (255,255,255),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),1,border_radius=15)
    change_char_surf = settings_buttons_font.render("Change Character",1,(255,255,255))
    pos_text = ((1300/2 - 2*marge_buttons_settings)/2 - change_char_surf.get_width()//2 + marge_buttons_settings , 2*marge_buttons_settings + 30 - change_char_surf.get_height()//2)
    screen.blit(change_char_surf,pos_text)

    pygame.display.update()

    continuer = True
    while(continuer):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True