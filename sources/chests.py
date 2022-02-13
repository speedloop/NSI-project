import pygame
from sources.constantes import *

def get_chests(room_map):
    chests_rects = []
    for i in range(len(room_map)):
        for j in range(len(room_map[i])):
            if room_map[i][j] == '?':
                chests_rects.append(pygame.rect.Rect((j*taille_cases+10,i*taille_cases+12,taille_cases,taille_cases)))
                
    return chests_rects
        
def matrix_pos(chest_rect):
    i = (chest_rect[1]-12)//taille_cases
    j = (chest_rect[0]-10)//taille_cases
    
    return (i,j)

def player_on_chest(room_map,pos_player):
    
    player_rect = pygame.rect.Rect(pos_player+(largeur_personnage,hauteur_personnage))
    
    chests_rects = get_chests(room_map)
    
    for chest in chests_rects:
        if player_rect.colliderect(chest):
            return matrix_pos(chest)
            
    return False