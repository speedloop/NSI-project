from constantes import *

def get_position_in_matrix(player_pos):
    j = (player_pos[0] - 10) / taille_cases
    i = (player_pos[1] - 12) / taille_cases
    return (int(j),int(i))
    
    


def test_collide(player_pos,map,direction):
    """retourne True si le personnage peut avancer sans foncer dans un mur, sinon, retourne False"""
    
    haut_droite = (player_pos[0] + 19, player_pos[1])
    bas_droite = (player_pos[0] + 19,player_pos[1] + 20)
    haut_gauche = player_pos
    bas_gauche = (player_pos[0],player_pos[1] + 20)
    
    if direction == "GAUCHE":
        #teste si le personnage peut aller à droite
        haut_droite = get_position_in_matrix(haut_droite)
        bas_droite = get_position_in_matrix(bas_droite)
        if map[haut_droite[1]][haut_droite[0]-1] == '#' or map[bas_droite[1]][bas_droite[0]-1] == '#':
            return False
        else: return True
        
    if direction == "DROITE":
        #teste si le personnage peut aller à droite
        haut_gauche = get_position_in_matrix(haut_gauche)
        bas_gauche = get_position_in_matrix(bas_gauche)
        if map[haut_gauche[1]][haut_gauche[0]+1] == '#' or map[bas_gauche[1]][bas_gauche[0]+1] == '#':
            return False
        else: return True
    
    if direction == "HAUT":
        #teste si le personnage peut aller à droite
        bas_droite = get_position_in_matrix(bas_droite)
        bas_gauche = get_position_in_matrix(bas_gauche)
        if map[bas_droite[1]-1][bas_droite[0]] == '#' or map[bas_gauche[1]-1][bas_gauche[0]] == '#':
            return False
        else: return True
        
    if direction == "BAS":
        #teste si le personnage peut aller à droite
        haut_gauche = get_position_in_matrix(haut_gauche)
        haut_droite = get_position_in_matrix(haut_droite)
        if map[haut_gauche[1]+1][haut_gauche[0]] == '#' or map[haut_droite[1]+1][haut_droite[0]] == '#':
            return False
        else: return True