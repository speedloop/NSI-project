from pydoc import render_doc
import pygame,os,random
from collide import test_collide
from constantes import *

def get_map_from_file(path_to_file):
    with open(path_to_file,'r') as file:
        map = file.readlines()
        for i in range(len(map)):
            map[i] = map[i].rstrip('\n')
        file.close()
    return map
    
def get_player_initial_pos(map):
    for ligne in map:
        for case in ligne:
            if case == '@':
                i = map.index(ligne)
                j = ligne.index(case)
                return j*taille_cases+10 - (largeur_personnage//2) + taille_cases//2,i*37+12-(hauteur_personnage//2)+taille_cases//2

def get_nb_dongeon_maps():
    files = os.listdir(os.getcwd()+"/map")
    nb_maps = 0
    for file in files:
        if "carte" in file:
            nb_maps += 1
    return nb_maps


def display_room(screen,map_room):
    screen.fill((0,0,0))

    dict_textures = {
        '#': pygame.transform.scale(pygame.image.load("wall.png"),(taille_cases,taille_cases)),
        '.': pygame.transform.scale(pygame.image.load("empty.png"),(taille_cases,taille_cases)),
        '_': pygame.transform.scale(pygame.image.load("floor.png"),(taille_cases,taille_cases)),
        '@': pygame.transform.scale(pygame.image.load("spawner.png"),(taille_cases,taille_cases)),
        ':': pygame.transform.scale(pygame.image.load("floor.png"),(taille_cases,taille_cases)),
        '!': pygame.transform.scale(pygame.image.load("floor.png"),(taille_cases,taille_cases)),
        '?': pygame.transform.scale(pygame.image.load("chest.jpg"),(taille_cases,taille_cases))
    }

    for i in range(len(map_room)):
        for j in range(len(map_room[i])):
            screen.blit(dict_textures[map_room[i][j]], (taille_cases*j+10,taille_cases*i+12))
            
            if map_room[i][j] == '!': #mob
                pos_mob = (taille_cases*j+10,taille_cases*i+12)
                screen.blit(pygame.transform.scale(pygame.image.load("mobs/snowman.png"),(32,37)), pos_mob)

pygame.font.init()

def vie(viest,viechangement):
    nbvies= viechangement+int(viest)
    if nbvies>9:
        nbvies=9
    return (str(nbvies))

def game(screen):
    clock = pygame.time.Clock()
    
    nb_maps = get_nb_dongeon_maps()
    dongeon_map_number = str(random.randint(1,nb_maps))


    path_to_map = "rooms/lobby/lobby"
    map = get_map_from_file(path_to_map)
    
    vies='3'
    font_vies = pygame.font.Font("bouton.ttf",60)
    v=font_vies.render(vies,1,(255,50,50))
    vies_rect = pygame.rect.Rect((len(map)*taille_cases+10,12,v.get_width(),v.get_height()))
    screen.blit(v,vies_rect)
    
    x_player,y_player = get_player_initial_pos(map)    
    player = pygame.transform.scale(pygame.image.load("characters/spartan.png"),(largeur_personnage,hauteur_personnage))

    up,down,right,left = False,False,False,False
    
    
    
    
    
    
    #gestion des évènements
    continuer = True
    while continuer:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    return True
                if event.key == pygame.K_DOWN:
                    down = False                    
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
                    
                    
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_DOWN:
                    down = True                    
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_LEFT:
                    left = True
                    
        if left :  #si fleche gauche enfoncee 
            if test_collide((x_player-speed,y_player), map,"GAUCHE",screen):  #si le personnage ne collide pas avec un mur si il se deplace a gauche
                x_player -= speed
        if right : #si fleche droite enfoncee 
            if test_collide((x_player+speed,y_player),map, "DROITE",screen): #si le personnage ne collide pas avec un mur si il se deplace a droite
                x_player += speed
        if up:    #si fleche haut enfoncee 
            if test_collide((x_player,y_player-speed),map, "HAUT",screen):   #si le personnage ne collide pas avec un mur si il se deplace en haut
                y_player -= speed
        if down:  #si fleche bas enfoncee 
            if test_collide((x_player,y_player+speed),map, "BAS",screen):    #si le personnage ne collide pas avec un mur si il se deplace en bas
                y_player += speed
        
        
        display_room(screen,map)
        screen.blit(player,(x_player,y_player))
        screen.blit(v,vies_rect)
        pygame.display.update()



    return True
