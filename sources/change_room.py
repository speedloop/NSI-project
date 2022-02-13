import pygame

from sources.constantes import *

def change_room(dungeon, pos_in_dungeon, pos_player,exits):
    x_dungeon = pos_in_dungeon[0]
    y_dungeon = pos_in_dungeon[1]
    x_player = pos_player[0]
    y_player = pos_player[1]
    if exits[0] == True:   #personnage sur sortie ouest
        y_dungeon -= 1
        x_player += 17*taille_cases
    elif exits[1] == True:   #personnage sur sortie nord
        x_dungeon -= 1
        y_player += 19*taille_cases
    elif exits[2] == True:   #personnage sur sortie est
        y_dungeon += 1
        x_player -= 17*taille_cases
    elif exits[3] == True:   #personnage sur sortie sud
        x_dungeon += 1
        y_player -= 19*taille_cases
    pos_in_dungeon = (x_dungeon,y_dungeon)
    return pos_in_dungeon,(x_player,y_player)