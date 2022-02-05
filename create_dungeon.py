import os
from random import randint
from constantes import *


def get_map_from_file(path_to_file):
    """deduis une carte a partir d'un fichier codifié"""
    with open(path_to_file,'r') as file:
        map = file.readlines()
        for i in range(len(map)):
            map[i] = map[i].rstrip('\n')
        file.close()
    return map
    
    
def tirage_salle(path):
    """retournes une salle tirée au hasard parmi les salles du type choisi (honrizontale, verticale, cul-de-sac...)"""
    files = os.listdir(os.getcwd()+'/'+path)
    nb_salle = len(files)
    
    return files[randint(1,nb_salle)-1] 



def create_dungeon(dungeon_map):
    """retourne un dictionnaire des salles correspondant à chaque position dans le donjon"""
    dungeon = {}
    
    for i in range(len(dungeon_map)):
        for j in range(len(dungeon_map[i])):
            if dungeon_map[i][j] != '-':   #c'est une salle
                dungeon[(i,j)] = dict_salles[dungeon_map[i][j]]+tirage_salle(dict_salles[dungeon_map[i][j]])
                
    for key in dungeon.keys():
        map = get_map_from_file(dungeon[key])
        dungeon[key] = map
                
     
    return dungeon
    
    
    
def init_pos_dungeon(dungeon):
    for key in dungeon.keys():
        map = dungeon[key]
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == '@': #spawn trouvé
                    return key        