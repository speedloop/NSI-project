from pydoc import render_doc
from tkinter import EventType
from turtle import Screen
import pygame,os,random,time

from collide import test_collide
from constantes import *
from create_dungeon import *


def get_map_from_file(path_to_file):
    """deduis une carte a partir d'un fichier codifié"""
    with open(path_to_file,'r') as file:
        map = file.readlines()
        for i in range(len(map)):
            map[i] = map[i].rstrip('\n')
        file.close()
    return map
    
def get_player_initial_pos(map):
    """initialise la position du personnage sur le point de spawn"""
    for ligne in map:
        for case in ligne:
            if case == '@':
                i = map.index(ligne)
                j = ligne.index(case)
                return j*taille_cases+10 - (largeur_personnage//2) + taille_cases//2,i*37+12-(hauteur_personnage//2)+taille_cases//2

def get_nb_dungeon_maps():
    """retournes le nombre de carte de donjon"""
    files = os.listdir(os.getcwd()+"/map")
    nb_maps = 0
    for file in files:
        if "carte" in file:
            nb_maps += 1
    return nb_maps


def display_room(screen,map_room):
    """Cette fonction affiche la salle en fontion de ce qui est encode dans le fichier choisi"""
    screen.fill((0,0,0))

    for i in range(len(map_room)):
        for j in range(len(map_room[i])):
            screen.blit(dict_textures[map_room[i][j]], (taille_cases*j+10,taille_cases*i+12))
            
            if map_room[i][j] == '!': #c'est un mob
                pos_mob = (taille_cases*j+10,taille_cases*i+12)
                screen.blit(mob_surf, pos_mob)

pygame.font.init()

def vie(viest,viechangement):
    """Cette fonction prends en variable le nombre de vies initial et la difference, et retourne le nombre de vies finales, 
    pas plus de 9 vies"""
    nbvies= viechangement+int(viest)
    if nbvies>9:
        nbvies=9
    return (str(nbvies))


def game(screen):
    '''Fonction pricipale du jeu actif'''
    clock = pygame.time.Clock()
    
    nb_maps = get_nb_dungeon_maps()
    dungeon_map_number = str(random.randint(1,nb_maps))
    dungeon_map = get_map_from_file("map/carte "+dungeon_map_number)
    dungeon = create_dungeon(dungeon_map)
    

 #Temporaire, avant que le systeme de map sera entierement implemente, affice la salle choisie ---
    path_to_map = "rooms/lobby/lobby"
    map = get_map_from_file(path_to_map)
 #-----------------------------------------------------------------------

    x_player,y_player = get_player_initial_pos(map)    
    player = pygame.transform.scale(pygame.image.load("characters/spartan.png"),(largeur_personnage,hauteur_personnage))

    up,down,right,left = False,False,False,False
    
    #Affichage des vies initial-----
    vies='3'
    font_vies = pygame.font.Font("fonts/bouton.ttf",60)
    v=font_vies.render(vies,1,(255,50,50))
    vies_rect = pygame.rect.Rect((len(map)*taille_cases+10,12,v.get_width(),v.get_height()))
    coeur = pygame.transform.scale(pygame.image.load("textures/heart.png"),(v.get_height(),v.get_height()))
    coeur_rect = pygame.rect.Rect((len(map)*taille_cases+20+v.get_width(),12,v.get_height(),v.get_height()))
    #---------------------------------

    #Partie principale du jeu qui tourne en permanence:
    continuer = True
    while continuer:
        clock.tick(30)
        #Gestions des touches en jeu----------------------
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
                if event.key == pygame.K_KP_PLUS:
                    vies=vie(vies,1)
                    v=font_vies.render(vies,1,(255,50,50))
                    screen.blit(v,vies_rect)
                if event.key == pygame.K_KP_MINUS:
                    vies=vie(vies,-1)
                    v=font_vies.render(vies,1,(255,50,50))
                    screen.blit(v,vies_rect)

        #--------------------------------------------------------

                    
        if left :  #si fleche gauche enfoncee 
            if test_collide((x_player-speed,y_player), map,"GAUCHE",screen):  #si le personnage ne collide pas avec un mur si il se deplace a gauche
                x_player -= speed
            else:
                print("collide")
        if right : #si fleche droite enfoncee 
            if test_collide((x_player+speed,y_player),map, "DROITE",screen): #si le personnage ne collide pas avec un mur si il se deplace a droite
                x_player += speed
            else:
                print("collide")
        if up:    #si fleche haut enfoncee 
            if test_collide((x_player,y_player-speed),map, "HAUT",screen):   #si le personnage ne collide pas avec un mur si il se deplace en haut
                y_player -= speed
            else:
                print("collide")
        if down:  #si fleche bas enfoncee 
            if test_collide((x_player,y_player+speed),map, "BAS",screen):    #si le personnage ne collide pas avec un mur si il se deplace en bas
                y_player += speed
            else:
                print("collide")
        
        #Ecran game over----------------------------
        if vies == "0":
                screen.fill((0,0,0))
                mort_font = pygame.font.Font("fonts/title.ttf",64)
                mort_titre = mort_font.render("YOU ARE DEAD...",1,(255,255,255))
                mort_rect=vies_rect = ((50,12,v.get_width(),v.get_height()))                
                screen.blit(mort_titre,mort_rect)
                
                quit_font = pygame.font.Font("fonts/title.ttf",20)
                message_quit = mort_font.render("Press 'q' to restart",1,(255,255,255))
                screen.blit(message_quit,(750,700))
                
                pygame.display.update()
                ecranmort = 0
                while ecranmort == 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return False
                        if event.type == pygame.KEYDOWN: 
                            if event.key == pygame.K_q:
                                return True
        #-----------------------------------------
    
                
        display_room(screen,map)
        screen.blit(player,(x_player,y_player))
        screen.blit(v,vies_rect)
        screen.blit(coeur,coeur_rect)
        pygame.display.update()


    return True
