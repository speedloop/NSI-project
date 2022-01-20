from constantes import *
import pygame

def get_position_in_matrix(player_pos):
    j = (player_pos[0] - 10) / taille_cases
    i = (player_pos[1] - 12) / taille_cases
    return (int(j),int(i))
    
    
def get_walls_rect(map):
    walls_rect = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '#':
                walls_rect.append((j*taille_cases+10,i*taille_cases+12,taille_cases,taille_cases))
                
    return walls_rect
    
    


def test_collide(player_pos,map,direction,screen):
    """retourne True si le personnage peut avancer sans foncer dans un mur, sinon, retourne False, boolean"""
    
    haut_droite = (player_pos[0] + largeur_personnage, player_pos[1])
    bas_droite = (player_pos[0] + largeur_personnage,player_pos[1] + hauteur_personnage)
    haut_gauche = player_pos
    bas_gauche = (player_pos[0],player_pos[1] + hauteur_personnage)
    player_rect = pygame.rect.Rect(haut_gauche+(largeur_personnage,hauteur_personnage))
    
    walls_rect = get_walls_rect(map)
    
    for wall in walls_rect:
        if player_rect.colliderect(wall):
            return False
    return True
    
    