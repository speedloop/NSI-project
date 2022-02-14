import pygame 
from sources.game import *
from sources.settings import settings
from sources.constantes import *



def test_collide(mouse_pos,playrect):
    '''Verifie les colision. Si il en a une retourne True, booleen'''
    if playrect.collidepoint(mouse_pos):
        return True
    return False
    
def display_screen(screen, surfaces,rects):
    """Permet d'afficher plusieurs objets en meme temps. """
    for i in range(len(surfaces)):
        ecran.blit(surfaces[i],rects[i])
    pygame.display.update()
    
    

#Creations des textes dans le menu (titre,play,quit)----------------

pygame.font.init()

ecran = pygame.display.set_mode((1300,800))
ecran.fill((80,80,80))

clock = pygame.time.Clock()

font = pygame.font.Font("fonts/bouton.ttf",60)
play = font.render("PLAY", 1,(250,250,250))
play_rect = pygame.rect.Rect((50,650,play.get_width(),play.get_height()))
quit = font.render("QUIT",1,(250,250,250))
quit_rect = pygame.rect.Rect((50,730,quit.get_width(),quit.get_height())) 

font_title = pygame.font.Font("fonts/title.ttf",64)
title_surf = font_title.render("DOOMED SOULS",1,(255,255,255))

settings_pos = (1300-(settings_icon.get_width()+10),10)
settings_rect = pygame.rect.Rect(settings_pos + (settings_icon.get_width(),settings_icon.get_height()))

#--------------------------------------

quit_selected = False
play_selected = False
settings_selected = False


continuer = True

#Partie du code qui fait fonctionner le menu--------

while continuer:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False        
                
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            ecran.fill((80,80,80))
            #Affichage des rectangles autour des bouttons lors d'une collision
            if test_collide(mouse_pos, play_rect):                
                play_selected = True
            else: 
                play_selected = False
            if test_collide(mouse_pos,quit_rect):
                quit_selected = True
            else: 
                quit_selected = False

            #affiche d'un rectangle de sélection autour de l'icône des réglages
            if test_collide(mouse_pos,settings_rect):
                settings_selected = True
            else: 
                settings_selected = False
                
            
        #Execution des actions lors de la pression d'un des bouttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_selected:
                continuer = False
            if play_selected:
                continuer = game(ecran)
            if settings_selected:
                continuer = settings(ecran)
                
    #affichage du menu 
    ecran.fill((80,80,80))
    if quit_selected:   #affichage d'un "rectangle de sélection" autour du bouton quit si la souris est dessus
        pygame.draw.rect(ecran,(0,0,0),(45,735,quit.get_width()+15,60),border_radius=5) 
    if play_selected:   #affichage d'un "rectangle de sélection" autour du bouton play si la souris est dessus
        pygame.draw.rect(ecran,(0,0,0),(45,655,play.get_width()+15,60),border_radius=5)
    if settings_selected:
        pygame.draw.rect(ecran,(0,0,0),(settings_pos[0]-5,settings_pos[1]-5,settings_icon.get_width()+10,settings_icon.get_height()+10),border_radius = 5)
    display_screen(ecran, [play,quit,title_surf,settings_icon],[(50,650),(50,730),(ecran.get_width()/2-title_surf.get_width()/2,100),settings_pos])    
            
pygame.quit()