import pygame,os,random,time

from sources.collide import test_collide
from sources.detect_exit import detect_exit
from sources.change_room import change_room
from sources.chests import player_on_chest
from sources.create_dungeon import create_dungeon,init_pos_dungeon
from sources.constantes import *
from sources.objets import *


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


class Player:
    def __init__(self,surf,pos_x,pos_y,id):
        self.id = id #nom du personnage (ex : spartan,santa,savan...)
        self.initial_surf = surf
        self.current_frame = self.initial_surf
        self.right_surf = self.initial_surf #surface du personnage quand il se deplace vers la droite
        self.left_surf = pygame.transform.flip(self.initial_surf,True,False)  #surface du personnage quand il se deplace vers la droite

        self.direction = "DROITE"
        self.x = pos_x
        self.y = pos_y

        self.attack_frames = {
            "DROITE": [],
            "GAUCHE": []
        }
        self.attack_frames["DROITE"].append(pygame.image.load("animations/attack "+id+"/0.png")) #frame 1 importation
        self.attack_frames["DROITE"].append(pygame.image.load("animations/attack "+id+"/1.png")) #frame 2 importation
        self.attack_frames["DROITE"].append(pygame.image.load("animations/attack "+id+"/2.png")) #frame 3 importation
        self.attack_frames["DROITE"].append(pygame.image.load("animations/attack "+id+"/3.png")) #frame 4 importation
        self.attack_frames["GAUCHE"].append(pygame.transform.flip(pygame.image.load("animations/attack "+id+"/0.png"),True,False)) #frame 1 importation
        self.attack_frames["GAUCHE"].append(pygame.transform.flip(pygame.image.load("animations/attack "+id+"/1.png"),True,False)) #frame 2 importation
        self.attack_frames["GAUCHE"].append(pygame.transform.flip(pygame.image.load("animations/attack "+id+"/2.png"),True,False)) #frame 3 importation 
        self.attack_frames["GAUCHE"].append(pygame.transform.flip(pygame.image.load("animations/attack "+id+"/3.png"),True,False)) #frame 4 importation
        print(self.attack_frames)
        self.attack = False
        self.attack_frame = 0
        self.width = self.initial_surf.get_width()
        self.height = self.initial_surf.get_height()
        self.rect = pygame.rect.Rect((self.x,self.y,self.width,self.height))

    def turn(self,direction):
        if direction == "DROITE":
            self.current_frame = self.right_surf
            self.direction = "DROITE"
        else:
            self.current_frame = self.left_surf
            self.direction = "GAUCHE"

    def update_pos(self,new_x,new_y):
        self.x = new_x
        self.y = new_y

    def start_attack(self):
        self.attack = True

    def update_attack(self):
        if self.attack == True:
            self.current_frame = self.attack_frames[self.direction][int(self.attack_frame)]
            self.attack_frame += 0.5
            if int(self.attack_frame) == len(self.attack_frames[self.direction]): #dernière frame deja utilisée
                self.attack_frame = 0
                self.attack = False

pygame.font.init()


def game(screen,player_id):
    '''Fonction pricipale du jeu actif'''
    clock = pygame.time.Clock()
    
    nb_maps = get_nb_dungeon_maps()
    dungeon_map_number = str(randint(1,nb_maps))
    dungeon_map = get_map_from_file("map/carte "+dungeon_map_number)
    dungeon = create_dungeon(dungeon_map)
    dungeon_pos = init_pos_dungeon(dungeon)
    print(dungeon_pos)
    for key in dungeon.keys():
        print(key)
        for ligne in dungeon[key]:
            print(ligne)
    

 #Temporaire, avant que le systeme de map sera entierement implemente, affice la salle choisie ---
    path_to_map = "rooms/lobby/lobby"
    map = get_map_from_file(path_to_map)
 #-----------------------------------------------------------------------
    room_surface = pygame.draw.rect(screen,(0,0,0),(10,12,19*taille_cases,21*taille_cases))

    x_player,y_player = get_player_initial_pos(map)    
    player = Player(pygame.image.load("equiped_characters/"+player_id+".png"),x_player,y_player,player_id)

    up,down,right,left = False,False,False,False
    
    #Creation des variables non constantes, utilise dans les systemes de vie et d'inventaire
    vnc = {
    "vies" : 100, "vies_max": 100, "defense" : 0, "speed": 5, "inventaire" : [objets["..."]]*9  #inventaire rempli par neuf items "vide"...
    }
    #Affichage des vies initial-----
    
    vies_a_afficher=str(vnc["vies"])+" / "+str(vnc["vies_max"])
    vies_surf=berp_font.render(str(vies_a_afficher),1,(255,50,50))
    vies_pos = (20*taille_cases,12)
    vies_surf_pour_calcs=berp_font.render(("888 / 888"),1,(255,50,50))
    coeur_pos = (20*taille_cases + vies_surf_pour_calcs.get_width(),12)
    defense_surf = berp_font.render(str(vnc["defense"]),1,(255,50,50))
    defense_pos = (20*taille_cases + vies_surf_pour_calcs.get_width() + heart.get_width() + 200,12)
    shield_pos = (20*taille_cases + vies_surf_pour_calcs.get_width() + heart.get_width() + defense_surf.get_width() + 207,8)
     
    #-------------------------------------------------------


    #Partie principale du jeu qui tourne en permanence:
    continuer = True
    on_chest = False
    while continuer:
        clock.tick(20)
        print(clock.get_fps())
        exits = detect_exit(map,(player.x,player.y))
        on_chest = player_on_chest(dungeon[dungeon_pos],(player.x,player.y))
                            
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
                if event.key == pygame.K_a: #lancement attaque joueur
                    player.start_attack()
                if event.key == pygame.K_SPACE:
                    if True in exits: #le personnage se trouve sur une des sorties
                        dungeon_pos,pos_player = change_room(dungeon,dungeon_pos,(player.x,player.y),exits)
                        player.update_pos(pos_player[0],pos_player[1])
                        map = dungeon[dungeon_pos] 
                         
                if event.key == pygame.K_e:
                    if on_chest != False: #le personnage collide avec un coffre
                        line = map[on_chest[0]]
                        new_line = line[:on_chest[1]] + '^'+line[on_chest[1]+1:]
                        map[on_chest[0]] = new_line
                        dungeon[dungeon_pos] = map
                        on_chest = False
                        vnc["inventaire"] = ajout_objet_inv(vnc["inventaire"],screen) #variable objets dans objets.py
                        if vnc["inventaire"] == False: #au cas où on appuie sur la croix dans ajout_objet_inv()
                            return False
                        
                if event.key == pygame.K_DOWN:                    
                    down = True                    
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_RIGHT:
                    player.turn("DROITE")
                    right = True
                if event.key == pygame.K_LEFT:
                    player.turn("GAUCHE")
                    left = True
            
            # Gestion de l'inventaire -------------
                if event.key == pygame.K_1:
                   vnc = consommation_objet(0,vnc)
                if event.key == pygame.K_2:
                    vnc = consommation_objet(1,vnc)
                if event.key == pygame.K_3:
                    vnc = consommation_objet(2,vnc)
                if event.key == pygame.K_4:
                    vnc = consommation_objet(3,vnc)
                if event.key == pygame.K_5:
                    vnc = consommation_objet(4,vnc)
                if event.key == pygame.K_6:
                    vnc = consommation_objet(5,vnc)
                if event.key == pygame.K_7:
                    vnc = consommation_objet(6,vnc)
                if event.key == pygame.K_8:
                    vnc = consommation_objet(7,vnc)
                if event.key == pygame.K_9:
                    vnc = consommation_objet(8,vnc)
            
            #Cheats pour les vies -----------------------------------------------------
                if event.key == pygame.K_KP_PLUS:
                    vnc["vies"]=viechange(vnc["vies"],vnc["vies_max"],vnc["defense"],1)
                if event.key == pygame.K_KP_MINUS:
                    vnc["vies"]=viechange(vnc["vies"],vnc["vies_max"],vnc["defense"],-1)
            #Cheats pour la defense --------------------------------------------------
                if event.key == pygame.K_KP_MULTIPLY:
                    vnc["defense"]+=1
                    if vnc["defense"]<0:
                        vnc["defense"] = 0
                    if vnc["defense"] > 99:
                        vnc["defense"] = 99
                    defense_surf = berp_font.render(str(vnc["defense"]),1,(255,50,50))
                    shield_pos = (20*taille_cases + vies_surf_pour_calcs.get_width() + heart.get_width() + defense_surf.get_width() + 207,8)
                if event.key == pygame.K_KP_DIVIDE:
                    vnc["defense"]-=1
                    if vnc["defense"]<0:
                        vnc["defense"] = 0
                    if vnc["defense"] > 99:
                        vnc["defense"] = 99
                    defense_surf = berp_font.render(str(vnc["defense"]),1,(255,50,50))
                    shield_pos = (20*taille_cases + vies_surf_pour_calcs.get_width() + heart.get_width() + defense_surf.get_width() + 207,8)
                #Cheat inventaire ---------------------------------
                if event.key == pygame.K_MINUS:
                    print("minus")
                    vnc["inventaire"] = ajout_objet_inv(vnc["inventaire"],screen)
                    if vnc["inventaire"] == False:
                        return False


        #--------------------------------------------------------

                    
        if left :  #si fleche gauche enfoncee 
            if test_collide((player.x-vnc["speed"],player.y), map):  #si le personnage ne collide pas avec un mur si il se deplace a gauche
                player.update_pos(player.x - vnc["speed"],player.y)
        if right : #si fleche droite enfoncee 
            if test_collide((player.x+vnc["speed"],player.y),map): #si le personnage ne collide pas avec un mur si il se deplace a droite
                player.update_pos(player.x + vnc["speed"],player.y)
        if up:    #si fleche haut enfoncee 
            if test_collide((player.x,player.y-vnc["speed"]),map):   #si le personnage ne collide pas avec un mur si il se deplace en haut
                player.update_pos(player.x,player.y - vnc["speed"])
        if down:  #si fleche bas enfoncee 
            if test_collide((player.x,player.y+vnc["speed"]),map):    #si le personnage ne collide pas avec un mur si il se deplace en bas
                player.update_pos(player.x,player.y + vnc["speed"])
        
        #Ecran game over----------------------------
        if vnc["vies"] < 1:
                screen.fill((0,0,0))
                mort_font = pygame.font.Font("fonts/optimus.ttf",64)
                mort_titre = mort_font.render("YOU ARE DEAD...",1,(255,255,255))
                mort_rect= (50,12,vies_surf.get_width(),vies_surf.get_height())                
                screen.blit(mort_titre,mort_rect)
                
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
        
        if player.attack == True:
            player.update_attack()
        screen.blit(player.current_frame,(player.x,player.y)) 
        pygame.draw.rect(screen,(0,0,0),(19*taille_cases+20,20*taille_cases+12,1300-(19*taille_cases+30),800-(20*taille_cases+24)))
        pygame.draw.rect(screen,(255,255,255),(19*taille_cases+20,20*taille_cases+12,1300-(19*taille_cases+30),800-(20*taille_cases+24)),1,border_radius = 40)
        if True in exits: #le personnage est sur une sortie
            travel_tip = tip_font.render("Press space to travel",1,(255,255,255))
            screen.blit(travel_tip,(19*taille_cases+30,20*taille_cases+12))
        elif on_chest != False:
            chest_tip = tip_font.render("Press 'e' to open chest",1,(255,255,255))
            screen.blit(chest_tip,(19*taille_cases+30,20*taille_cases+12))

        
        affichage_inventaire(vnc["inventaire"],screen)

        vies_surf=berp_font.render(str(str(vnc["vies"])+" / "+str(vnc["vies_max"])),1,(255,50,50))
        screen.blit(vies_surf,vies_pos)
        screen.blit(heart,coeur_pos)
        screen.blit(shield_icon,shield_pos)
        screen.blit(defense_surf,defense_pos)
        
        pygame.display.update()


    return True
