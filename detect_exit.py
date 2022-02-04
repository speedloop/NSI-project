import pygame

from constantes import *


def get_exits_rects(map_room):
    exits_rects = []
    for i in range(len(map_room)):
        for j in range(len(map_room[i])):
            if map_room[i][j] == ':':
                exits_rects.append((j*taille_cases+10,i*taille_cases+12,taille_cases,taille_cases))
    return exits_rects
    



def detect_exit(map_room,pos_player):
    
    character_on_exit = False
    
    possible_exit_rects = [
        (10,10*taille_cases+12,taille_cases,taille_cases),  #sortie ouest
        (9*taille_cases+10,12,taille_cases,taille_cases),   #sortie nord
        (18*taille_cases+10,10*taille_cases+12,taille_cases,taille_cases),  #sortie est
        (9*taille_cases+10,20*taille_cases+12,taille_cases,taille_cases)    #sortie sud
    ]
    
    exits_rects = get_exits_rects(map_room)
    
    player_rect = pygame.rect.Rect(pos_player + (largeur_personnage,hauteur_personnage))
    
    ouest,nord,est,sud = False,False,False,False
    
    for exit in exits_rects:
        if player_rect.colliderect(exit):
            character_on_exit = True
            
            if character_on_exit:
                if exit == possible_exit_rects[0]:        #personnage sur sortie ouest
                    ouest = True 
                elif exit == possible_exit_rects[1]:      #personnage sur sortie nord
                    nord = True
                elif exit == possible_exit_rects[2]:      #personnage sur sortie est
                    est = True
                elif exit == possible_exit_rects[3]:      #personnage sur sortie sud
                    sud = True
    return [ouest,nord,est,sud]