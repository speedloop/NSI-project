import pygame 
from game import *
from constantes import *



def test_collide(mouse_pos,playrect):
    '''Verifie les colision. Si il en a une retourne True, boolean'''
    if playrect.collidepoint(mouse_pos):
        return True
    return False
    
def display_screen(screen, surfaces,rects):
    """Permet d'afficher plusieurs objets en meme temps. S'utilise dans la fonction principale """
    for i in range(len(surfaces)):
        ecran.blit(surfaces[i],rects[i])
    pygame.display.update()
    
    

#Creations des textes dans le menu----------------

pygame.font.init()

ecran = pygame.display.set_mode((1300,800))
ecran.fill((80,80,80))

clock = pygame.time.Clock()

font = pygame.font.Font("bouton.ttf",60)
play = font.render("PLAY", 1,(250,250,250))
play_rect = pygame.rect.Rect((50,650,play.get_width(),play.get_height()))
quit = font.render("QUIT",1,(250,250,250))
quit_rect = pygame.rect.Rect((50,730,quit.get_width(),quit.get_height())) 

font_title = pygame.font.Font("title.ttf",64)
title_surf = font_title.render("DOOMED SOULS",1,(255,255,255))

pygame.display.update()

#--------------------------------------

salle = []

quit_selected = False
play_selected = False


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
                pygame.draw.rect(ecran,(0,0,0),(45,645,play.get_width()+15,60),border_radius=5)
                play_selected = True
            else: 
                play_selected = False
            if test_collide(mouse_pos,quit_rect):
                pygame.draw.rect(ecran,(0,0,0),(45,725,quit.get_width()+15,60),border_radius=5)
                quit_selected = True
            else: 
                quit_selected = False
                
            #Affiche les textes dans le menu avec la fonction dispalay_screen
            display_screen(ecran, [play,quit,title_surf],[(50,650),(50,730),(ecran.get_width()/2-title_surf.get_width()/2,100)])        
        #Execution des actions lors de la pression d'un des bouttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_selected:
                continuer = False
            if play_selected:
                continuer = game(ecran)
            
pygame.quit()