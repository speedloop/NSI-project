import pygame

from constantes import *

def change_room(dungeon, pos_in_dungeon, exits):
    x_dungeon = pos_in_dungeon[0]
    y_dungeon = pos_in_dungeon[1]
    if exits[0] == True:   #personnage sur sortie ouest
        y_dungeon -= 1
    elif exits[1] == True:   #personnage sur sortie nord
        x_dungeon += 1
    elif exits[2] == True:   #personnage sur sortie est
        y_dungeon += 1
    elif exits[3] == True:   #personnage sur sortie sud
        x_dungeon -= 1
    pos_in_dungeon = (x_dungeon,y_dungeon)
    return pos_in_dungeon