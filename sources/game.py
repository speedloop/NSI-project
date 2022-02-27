
import pygame,os,random,time
from queue import PriorityQueue
from math import sqrt

from sources.collide import test_collide,get_walls_rect
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


def create_room(room,map_room):
    """Cette fonction affiche la salle en fontion de ce qui est encode dans le fichier choisi"""
    room.fill((0,0,0))
    mobs = []

    for i in range(len(map_room)):
        for j in range(len(map_room[i])):
            room.blit(dict_textures[map_room[i][j]], (taille_cases*j,taille_cases*i))
            
            if map_room[i][j] == '!': #c'est un mob
                pos_mob = (taille_cases*j+10,taille_cases*i+12)
                mobs.append(Mob("snowman",pos_mob[0],pos_mob[1]))
    
    return mobs

def update_map(room_surface,i,j,new_element):
    """Prend en paramètre la surface de la salle, la position de l'élément à changer dans la matrice représentant la salle, et la nouvelle valeur de cet élément"""
    x = j * taille_cases
    y = i * taille_cases

    room_surface.blit(dict_textures[new_element],(x,y))

def set_neighbors(initial_pos):
    neighbors = []
    initial_x = initial_pos[0]
    initial_y = initial_pos[1]

    neighbors.append((initial_x + 5,initial_y))
    neighbors.append((initial_x - 5,initial_y))
    neighbors.append((initial_x + 5,initial_y+5))
    neighbors.append((initial_x + 5,initial_y-5))
    neighbors.append((initial_x - 5,initial_y-5))
    neighbors.append((initial_x - 5,initial_y+5))
    neighbors.append((initial_x,initial_y+5))
    neighbors.append((initial_x,initial_y-5))

    return neighbors

def distance(a_pos,b_pos):
    a_x = a_pos[0]
    a_y = a_pos[1]
    b_x = b_pos[0]
    b_y = b_pos[1]

    diff_x = max(a_x,b_x) - min(a_x,b_x)
    diff_y = max(a_y,b_y) - min(a_y,b_y)

    return sqrt(diff_x**2 + diff_y**2)
    


class Player:
    def __init__(self,surf,pos_x,pos_y,id):
        self.id = id #nom du personnage (ex : spartan,santa,savan...)
        self.initial_surf = surf
        self.current_frame = self.initial_surf
        self.right_surf = self.initial_surf #surface du personnage quand il se deplace vers la droite
        self.left_surf = pygame.image.load("equiped_characters/"+id+"/GAUCHE.png")
        self.top_surf = pygame.image.load("equiped_characters/"+id+"/HAUT.png")
        self.low_surf = pygame.image.load("equiped_characters/"+id+"/BAS.png")

        self.direction = "DROITE"
        self.x = pos_x
        self.y = pos_y
        self.width = self.initial_surf.get_width()
        self.height = self.initial_surf.get_height()

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
        self.attack = False
        self.attack_frame = 0
        self.width = self.initial_surf.get_width()
        self.height = self.initial_surf.get_height()
        self.rect = pygame.rect.Rect((self.x,self.y,self.width,self.height))

    def turn(self,direction):
        if direction == "DROITE":
            self.current_frame = self.right_surf
            self.direction = "DROITE"
        elif direction == "GAUCHE":
            self.current_frame = self.left_surf
            self.direction = "GAUCHE"
        elif direction == "HAUT":
            self.current_frame = self.top_surf
        else:
            self.current_frame = self.low_surf

    def update_pos(self,new_x,new_y):
        self.x = new_x
        self.y = new_y

    def start_attack(self):
        self.attack = True

    def update_attack(self):
        if self.attack == True:
            self.current_frame = self.attack_frames[self.direction][int(self.attack_frame)]
            self.attack_frame += 0.3
            if int(self.attack_frame) == len(self.attack_frames[self.direction]): #dernière frame deja utilisée
                self.attack_frame = 0
                self.attack = False
                
class Mob:
    def __init__(self,id,pos_x,pos_y):
        self.initial_surf = pygame.image.load("mobs/"+id+".png")
        self.current_frame = self.initial_surf
        self.right_surf = self.initial_surf
        self.left_surf = pygame.transform.flip(self.initial_surf,True,False)
        
        
        self.x = pos_x
        self.y = pos_y
        self.width = self.initial_surf.get_width()
        self.height = 32

        self.death = False
        self.death_frame = 0
        self.death_frames = [
            pygame.image.load("animations/death "+id+"/1.png"),
            pygame.image.load("animations/death "+id+"/2.png"),
            pygame.image.load("animations/death "+id+"/3.png"),
            pygame.image.load("animations/death "+id+"/4.png")
        ]
        self.direction = "DROITE"
        self.chemin = []

    def pathfiding(self,player,map_room,ecran):
        start = time.time()
        
        self.chemin = [[(self.x,self.y)]]        

        visited = [(self.x,self.y)]
        traites = []

        while not self.collide_player(player,self.chemin[-1][-1]):
            for i in range(len(self.chemin)):
                last_pos = self.chemin[i][-1]
                if last_pos not in traites:
                    traites.append(last_pos)
                    neighbors = set_neighbors(last_pos)
                    for neighbor in neighbors:
                        if not self.collide(map_room,neighbor) and neighbor not in visited and distance(neighbor,(player.x,player.y)) < distance(last_pos,(player.x,player.y))+2.5:
                            pygame.draw.rect(ecran,(255,255,255),pygame.rect.Rect(neighbor[0],neighbor[1],self.width,self.height))                            
                            pygame.display.update()
                            self.chemin.append(self.chemin[i]+[neighbor])
                            visited.append(neighbor)
        self.chemin = self.chemin[-1][1:]
        end = time.time()
        print(end-start)


    def collide_player(self,player,mob_pos):
        player_rect = pygame.rect.Rect(player.x,player.y,player.width,player.height)
        mob_rect = pygame.rect.Rect(mob_pos[0],mob_pos[1],self.width,self.height)

        if mob_rect.colliderect(player_rect):
            return True 
        return False

    def collide(self,map_room,neighbor):
        """retournes True si le mob collide avec un mur, sinon retournes False"""
        walls_rect = get_walls_rect(map_room)
        neighbor_rect = pygame.rect.Rect(neighbor[0],neighbor[1]+5,self.width,self.height)
        for wall in walls_rect:
            if neighbor_rect.colliderect(wall):
                return True
        return False



    def animate_death(self):
        self.death = True

    def update_death(self):
        if self.death:
            self.current_frame = self.death_frames[int(self.death_frame)]
            self.death_frame += 0.2
            if int(self.death_frame) == len(self.death_frames): #dernière frame deja utilisée
                self.death_frame = 0
                self.death = False
        
    def update_pos(self,new_x,new_y):
        self.x = new_x
        self.y = new_y
        
    def turn(self,direction):
        if direction == "DROITE":
            self.current_frame = self.right_surf
            self.direction = "DROITE"
        else:
            self.current_frame = self.left_surf
            self.direction = "GAUCHE"

pygame.font.init()


def game(screen,player_id):    
    '''Fonction pricipale du jeu actif'''
    screen.fill((0,0,0))
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
    
    room_surface = pygame.Surface((19*taille_cases,21*taille_cases))
    path_to_map = "rooms/lobby/lobby"
    map = get_map_from_file(path_to_map)
    mobs = create_room(room_surface,map)
    screen.blit(room_surface,(10,12))
    print(mobs)
   


    x_player,y_player = get_player_initial_pos(map)    
    player = Player(pygame.image.load("equiped_characters/"+player_id+"/DROITE.png"),x_player,y_player,player_id)

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
        clock.tick(30)
        exits = detect_exit(map,(player.x,player.y))
        on_chest = player_on_chest(dungeon[dungeon_pos],(player.x,player.y))
        
        ######################
        #---Pathfiding mob---#
        ######################
        if mobs != []:            
            mobs[0].pathfiding(player,map,screen)
            print(mobs[0].chemin)
        
                            
        #Gestions des touches en jeu----------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYUP:
                #if event.key == pygame.K_q:
                 #   return True
                if event.key == pygame.K_DOWN:
                    down = False                    
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
                    
                    
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_z:
                    if not mobs[0].collide(map,(mobs[0].x,mobs[0].y-5)):
                        mobs[0].update_pos(mobs[0].x,mobs[0].y-5)
                if event.key == pygame.K_q:
                    if not mobs[0].collide(map,(mobs[0].x-5,mobs[0].y)):
                        mobs[0].update_pos(mobs[0].x-5,mobs[0].y)
                if event.key == pygame.K_s:
                    if not mobs[0].collide(map,(mobs[0].x,mobs[0].y+5)):
                        mobs[0].update_pos(mobs[0].x,mobs[0].y+5)
                if event.key == pygame.K_d:
                    if not mobs[0].collide(map,(mobs[0].x+5,mobs[0].y)):
                        mobs[0].update_pos(mobs[0].x+5,mobs[0].y)


                if event.key == pygame.K_k:
                    mobs[0].animate_death()

                if event.key == pygame.K_a: #lancement attaque joueur
                    player.start_attack()
                
                if event.key == pygame.K_SPACE:
                    if True in exits: #le personnage se trouve sur une des sorties
                        dungeon_pos,pos_player = change_room(dungeon,dungeon_pos,(player.x,player.y),exits)
                        player.update_pos(pos_player[0],pos_player[1])
                        map = dungeon[dungeon_pos] 
                        screen.fill((0,0,0))
                        mobs = create_room(room_surface,map)
                         
                if event.key == pygame.K_e:
                    if on_chest != False: #le personnage collide avec un coffre
                        line = map[on_chest[0]]
                        new_line = line[:on_chest[1]] + '^'+line[on_chest[1]+1:]
                        map[on_chest[0]] = new_line
                        dungeon[dungeon_pos] = map
                        update_map(room_surface,on_chest[0],on_chest[1],'^')
                        on_chest = False
                        vnc["inventaire"] = ajout_objet_inv(vnc["inventaire"],screen) #variable objets dans objets.py
                        if vnc["inventaire"] == False: #au cas où on appuie sur la croix dans ajout_objet_inv()
                            return False
                        
                if event.key == pygame.K_DOWN:                    
                    down = True 
                    player.turn("BAS")                   
                if event.key == pygame.K_UP:
                    up = True
                    player.turn("HAUT")
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
        if right and not left:
            player.turn("DROITE")
        elif left and not right:
            player.turn("GAUCHE")
        elif up and not(right or left or down):
            player.turn('HAUT')
        elif down and not(right or left or up):
            player.turn("BAS")

        
        
            
        screen.fill((0,0,0))

        screen.blit(room_surface,(10,12))

        #Affichage des mobs
        for mob in mobs :
            if mob.chemin != []:
                new_pos = mob.chemin.pop(0)
                mob.update_pos(new_pos[0],new_pos[1])
            if mob.death:
                mob.update_death()
            screen.blit(mob.current_frame,(mob.x,mob.y))

        #Affichage du joueur
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
        coeur_pos = (vies_pos[0]+vies_surf.get_width()+10, vies_pos[1])
        screen.blit(heart,coeur_pos)
        screen.blit(shield_icon,shield_pos)
        screen.blit(defense_surf,defense_pos)
        
        pygame.display.update()


    return True
