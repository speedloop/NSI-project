import pygame
from sources.constantes import *

    
    
def get_walls_rect(map):
    """retournes tous les rects des murs qui constituent la salle"""
    walls_rect = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '#':
                walls_rect.append((j*taille_cases+10,i*taille_cases+12,taille_cases,taille_cases))
                
    return walls_rect
    
    


def test_collide(player_pos,map,direction):
    """retourne True si le personnage peut avancer sans foncer dans un mur, sinon, retourne False, boolean"""
       
    
    
    min_x = player_pos[0] + largeur_epee    
    min_y = player_pos[1]    
    max_x = min_x + largeur_personnage_sans_epee
    max_y = min_y + hauteur_personnage

    player_rect = pygame.rect.Rect((min_x,min_y,largeur_personnage_sans_epee,hauteur_personnage))   #definition d'une zone autour du personnage
    
    walls_rect = get_walls_rect(map)   #obtenir tous les rects (x,y,largeur,hauteur) des murs de la map
    
    for wall in walls_rect:
        #on parcours chaque rect de chaque mur
        if player_rect.colliderect(wall):  #si le personnage est en contact avec l'un d'entre eux :
            return False    #alors il ne peut pas avancer

    if max_x > 19*taille_cases+10: #le personnage va sortir de la map côté est
        return False
    if max_y > 21*taille_cases+12: #le personnage va sortir de la map côté sud
        return False
    if min_x < 10: #le personnage va sortir de la map côté est
        return False
    if min_y < 12: #le personnage va sortir de la map côté nord 
        return False
    
    return True  #feux vert
    
    