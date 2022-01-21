import pygame
from constantes import *

    
    
def get_walls_rect(map):
    """retournes tous les rects des murs qui constituent la salle"""
    walls_rect = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '#':
                walls_rect.append((j*taille_cases+10,i*taille_cases+12,taille_cases,taille_cases))
                
    return walls_rect
    
    


def test_collide(player_pos,map,direction,screen):
    """retourne True si le personnage peut avancer sans foncer dans un mur, sinon, retourne False, boolean"""
       
    player_rect = pygame.rect.Rect(player_pos+(largeur_personnage,hauteur_personnage))   #definition d'une zone autour du personnage
    
    walls_rect = get_walls_rect(map)   #obtenir tous les rects (x,y,largeur,hauteur) des murs de la map
    
    for wall in walls_rect:
        #on parcours chaque rect de chaque mur
        if player_rect.colliderect(wall):  #si le personnage est en contact avec l'un d'entre eux :
            return False    #alors il ne peut pas avancer
    return True  #feux vert
    
    