import pygame 
import os
from random import randint
from constantes import *

def tirage_salle(path):
    """retournes une salle tirée au hasard parmi les salles du type choisi (honrizontale, verticale, cul-de-sac...)"""
    files = os.listdir(os.getcwd()+path)
    nb_salle = len(files)
    
    return files[randint(1,nb_salle)-1] 



def create_dungeon(dungeon_map):
    """retourne un dictionnaire des salles correspondant à chaque position dans le donjon"""
    print(dungeon_map)
    dungeon = {}
    
    for i in range(len(dungeon_map)):
        for j in range(len(dungeon_map[i])):
            if dungeon_map[i][j] != '-':   #c'est une salle
                dungeon[(i,j)] = "rooms/"+dict_salles[dungeon_map[i][j]]+tirage_salle(dict_salles[dungeon_map[i][j]])
                
    print(dungeon)
    return dungeon
        