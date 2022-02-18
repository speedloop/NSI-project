import pygame,os,random
from sources.change_char import change_char
from sources.constantes import *


def settings(screen):
    new_character = False 


    pygame.display.update()

    change_char_selected = False
    random_char_selected = False
    done_button_selected = False

    continuer = True
    while(continuer):
        screen.fill((80,80,80))

        ###########################################
        #---Affichage button "change character"---#
        ###########################################
        change_char_rect = pygame.draw.rect(screen, (0,0,0),(marge_buttons_settings,2*marge_buttons_settings,1300/2 - 2*marge_buttons_settings,60),border_radius=15)
        if change_char_selected :#affichage du bouton en vert clair si la souris est au-dessus
            pygame.draw.rect(screen, (0,255,0),change_char_rect,1,border_radius=15)
            change_char_surf = settings_buttons_font.render("Change Character",1,(0,255,0))
        else: #affichage du bouton normal, en blanc
            pygame.draw.rect(screen, (255,255,255),change_char_rect,1,border_radius=15)
            change_char_surf = settings_buttons_font.render("Change Character",1,(255,255,255))
        
        pos_text_change_char = ((1300/2 - 2*marge_buttons_settings)/2 - change_char_surf.get_width()//2 + marge_buttons_settings , 2*marge_buttons_settings + 30 - change_char_surf.get_height()//2)
        screen.blit(change_char_surf,pos_text_change_char)

        #############################################
        #--Affichage du bouton "random character"---#
        #############################################
        random_char_rect = pygame.draw.rect(screen,(0,0,0),(1300//2+marge_buttons_settings,2*marge_buttons_settings,1300//2 - 2*marge_buttons_settings,60),border_radius = 15)
        if random_char_selected:
            pygame.draw.rect(screen,(0,255,0),random_char_rect,1,border_radius = 15)
            random_char_surf = settings_buttons_font.render("Random character",1,(0,255,0))
        else:
            pygame.draw.rect(screen,(255,255,255),random_char_rect,1,border_radius = 15)
            random_char_surf = settings_buttons_font.render("Random character",1,(255,255,255))

        pos_text_random_char = (random_char_rect[0] + random_char_rect[2]//2 - random_char_surf.get_width()//2 , random_char_rect[1] + random_char_rect[3]//2 - random_char_surf.get_height()//2)
        screen.blit(random_char_surf,pos_text_random_char)

        ##################################
        #---Affichage du bouton "DONE"---#
        ##################################
        done_button_surf = settings_done_button_font.render("DONE",1,(255,255,255))
        done_button_rect = pygame.draw.rect(screen,(0,0,0),(1300//2 - ((done_button_surf.get_width()+150)//2), 800 - 20 - done_button_surf.get_height(),done_button_surf.get_width()+150,done_button_surf.get_height()+10),border_radius = 15)
        if not done_button_selected:
            pygame.draw.rect(screen,(255,255,255),done_button_rect,1,border_radius = 15)
        else:
            pygame.draw.rect(screen, (0,255,0),done_button_rect,1,border_radius = 15)
            done_button_surf = settings_done_button_font.render("DONE",1,(0,255,0))
        pos_text_done = ((done_button_rect[0] + done_button_rect[2]//2 - done_button_surf.get_width()//2 , done_button_rect[1] + done_button_rect[3]//2 - done_button_surf.get_height()//2))
        screen.blit(done_button_surf,pos_text_done)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return pygame.transform.scale(new_character,(largeur_personnage,hauteur_personnage))

            if event.type == pygame.MOUSEMOTION:
                if change_char_rect.collidepoint(pygame.mouse.get_pos()): #souris sur bouton changement de personnage
                    change_char_selected = True
                else: change_char_selected = False
                if random_char_rect.collidepoint(pygame.mouse.get_pos()): #souris sur bouton personnage aléatoire
                    random_char_selected = True
                else: random_char_selected = False
                if done_button_rect.collidepoint(pygame.mouse.get_pos()):  #souris sur bouton done 
                    done_button_selected = True
                else: done_button_selected = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: #seulement le click gauche
                    if change_char_selected:
                        new_character = change_char(screen)
                        if new_character == False: return False
                    if random_char_selected:
                        new_character = pygame.image.load("characters/"+characters_img[random.randint(0,nb_personnages-1)])
                    if done_button_selected:
                        return pygame.transform.scale(new_character,(largeur_personnage,hauteur_personnage))


        

        pygame.display.update()    