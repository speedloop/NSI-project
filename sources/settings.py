import pygame
from sources.change_char import change_char
from sources.constantes import *

def settings(screen):
    screen.fill((80,80,80))    

    change_char_rect = pygame.draw.rect(screen, (0,0,0),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),border_radius=15)
    pygame.draw.rect(screen, (255,255,255),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),1,border_radius=15)
    change_char_surf = settings_buttons_font.render("Change Character",1,(255,255,255))
    pos_text = ((1300/2 - 2*marge_buttons_settings)/2 - change_char_surf.get_width()//2 + marge_buttons_settings , 2*marge_buttons_settings + 30 - change_char_surf.get_height()//2)
    screen.blit(change_char_surf,pos_text)

    pygame.display.update()

    change_char_selected = False

    continuer = True
    while(continuer):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True

            if event.type == pygame.MOUSEMOTION:
                if change_char_rect.collidepoint(pygame.mouse.get_pos()): #souris sur bouton changement de personnage
                    change_char_selected = True
                else: change_char_selected = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if change_char_selected:
                    continuer = change_char(screen)


        screen.fill((80,80,80))

        pygame.draw.rect(screen, (0,0,0),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),border_radius=15)
        if change_char_selected :#affichage du bouton en vert clair si la souris est au-dessus
            pygame.draw.rect(screen, (0,255,0),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),1,border_radius=15)
            change_char_surf = settings_buttons_font.render("Change Character",1,(0,255,0))
        else: #affichage du bouton normal, en blanc
            pygame.draw.rect(screen, (255,255,255),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),1,border_radius=15)
            change_char_surf = settings_buttons_font.render("Change Character",1,(255,255,255))
        screen.blit(change_char_surf,pos_text)

        pygame.display.update()    