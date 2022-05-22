
import pygame,os,random,time
import numpy as np
from queue import PriorityQueue
from math import sqrt,copysign

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
    walls = []

    for i in range(len(map_room)):
        for j in range(len(map_room[i])):
            if map_room[i][j] == '#':
                pos_wall = (taille_cases*j+10,taille_cases*i+12)
                walls.append(Wall(pos_wall[0],pos_wall[1]))

            room.blit(dict_textures[map_room[i][j]], (taille_cases*j,taille_cases*i))
            
            if map_room[i][j] == '!': #c'est un mob
                pos_mob = (taille_cases*j+10,taille_cases*i+12)
                mobs.append(Mob("snowman",pos_mob[0],pos_mob[1],(j,i)))
    
    return mobs,walls

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
    
    
def collide_walls(walls,pos):
    for wall in walls:
        if wall.collidepoint(pos):
            return True
    return False


class Wall:
    def __init__(self,pos_x,pos_y):
        self.x = pos_x
        self.y = pos_y
        self.rect = pygame.rect.Rect(self.x,self.y,taille_cases,taille_cases)
        
    def collidepoint(self,pos_point):
        if self.rect.collidepoint(pos_point):
            return True
        else: return False
    


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
        self.zone_frappe = pygame.rect.Rect(self.x+46,self.y+4,14,27)
        self.atk = 5
        self.dealt_dammages = False

    def turn(self,direction):
        if direction == "DROITE":
            self.current_frame = self.right_surf
            self.direction = "DROITE"            
            self.zone_frappe = pygame.rect.Rect(self.x+46,self.y+4,14,27)
        elif direction == "GAUCHE":
            self.current_frame = self.left_surf
            self.direction = "GAUCHE"
            self.zone_frappe = pygame.rect.Rect(self.x,self.y,14,27)
        elif direction == "HAUT":
            self.current_frame = self.top_surf
        else:
            self.current_frame = self.low_surf

    def update_pos(self,new_x,new_y):
        self.x = new_x
        self.y = new_y        
        if self.direction == "DROITE":
            self.zone_frappe = pygame.rect.Rect(self.x+46,self.y+4,14,27)
        if self.direction == "GAUCHE":            
            self.zone_frappe = pygame.rect.Rect(self.x,self.y,14,27)

    def start_attack(self):
        self.attack = True

    def update_attack(self):
        if self.attack == True:
            self.current_frame = self.attack_frames[self.direction][int(self.attack_frame)]
            self.attack_frame += 0.25
            if int(self.attack_frame) == len(self.attack_frames[self.direction]): #dernière frame deja utilisée
                self.attack_frame = 0
                self.attack = False
                self.dealt_dammages = False

    def collide_sword_mob(self,mob):
        mob_rect = pygame.rect.Rect(mob.x,mob.y,mob.width,mob.height)
        if self.zone_frappe.colliderect(mob_rect):
            return True
        else: return False
                
class Mob:
    def __init__(self,id,pos_x,pos_y,map_pos):  #map_pos = position dans la matrice de la map au moment du spawn
        self.speed = 5
    
        self.id = id 
        self.initial_surf = pygame.image.load("mobs/"+id+".png")
        self.current_frame = self.initial_surf
        self.right_surf = self.initial_surf
        self.left_surf = pygame.transform.flip(self.initial_surf,True,False)
        
        self.map_x,self.map_y = map_pos
        self.x = pos_x
        self.y = pos_y
        self.width = self.initial_surf.get_width()
        self.height = 32

        self.attack,self.defense,self.reach,self.lives = self.import_stats()

        self.death = False
        self.death_frame = 0
        self.death_frames = [
            pygame.image.load("animations/death "+id+"/1.png"),
            pygame.image.load("animations/death "+id+"/2.png"),
            pygame.image.load("animations/death "+id+"/3.png"),
            pygame.image.load("animations/death "+id+"/4.png")
        ]
        self.dead = False

        self.direction = "DROITE"
        self.next_pos = ()


    def take_dammage(self,player_atk):
        damages = player_atk - self.defense
        print("snowman takes ",damages,'damages')
        self.lives -= damages 
        if self.lives <= 0:
            self.animate_death()

    def import_stats(self):
        with open("stats_mobs/"+self.id+".stats",'r') as file:
            data = file.readlines()
            if data[0][0] == '#':
                data.pop(0)
            for i in range(len(data)): 
                data[i] = data[i].rstrip('\n')
            atk = int(data[0])
            deff =int(data[1])
            reach = int(data[2])
            lives = int(data[3])
            file.close()
        return atk,deff,reach,lives

    def ciblage(self,player,walls):
        """renvoie True si le mob peut viser le joueur, False sinon"""

        i_mob = (self.y[1]-12)//taille_cases
        j_mob = (self.x[0]-10)//taille_cases

        i_player = (player.y[1]-12)//taille_cases
        j_player = (player.x[0]-10)//taille_cases

        if i_mob == i_player or j_mob == j_player:
            return True
        else: 
            return False

        """vx = int(player.x - self.x)
        vy = int(player.y - self.y)

        for i in range(1,max(vx,vy),5):
            for wall in walls:
                if abs(vx) > abs(vy):
                    check_pos = (self.x + copysign(i,vx), self.y + copysign(i*vy/vx,vy))
                elif abs(vy) > abs(vx):
                    check_pos = (self.x + copysign(i*vx/vy,vx), self.y + copysign(i,vy))
                else:
                    check_pos = (self.x + copysign(i,vx), self.y + copysign(i,vy))

                check_rect = check_pos + (32,37)

                if wall.rect.colliderect(check_rect):
                    return False
        return True"""

        
    def easy_pathfiding(self, player, walls):
        
        vx = player.x - self.x
        vy = player.y - self.y  

        print("vx : ",vx)
        print("vy : ",vy)              

        if abs(vx) > abs(vy):   
            if vx > 0:                     
                next_x = self.x + 5
            else:
                next_x = self.x - 5

            if vy >= 0:
                next_y = self.y + (5 * vy/vx)                    
            else:
                next_y = self.y - (5 * vy/vx)

        elif abs(vy) > abs(vx):
            if vy > 0:                     
                next_y = self.y + 5
            else:
                next_y = self.y - 5

            if vx >= 0:
                next_x = self.x + (5 * vx/vy)                    
            else:
                next_x = self.x - (5 * vx/vy)
        else:
            if vx > 0:                     
                next_x = self.x + 5
            else:
                next_x = self.x - 5

            if vy >= 0:
                next_y = self.y + 5                  
            else:
                next_y = self.y - 5

        print("next_x : ", next_x)
        print("next_y : ", next_y)
                    
        collide_vx = False
        collide_vy = False
        collide_oppose_vx = False
        collide_oppose_vy = False
        
        for wall in walls:
            if wall.rect.collidepoint((self.x,next_y)): #collide côté vy
                collide_vy = True
            elif wall.rect.collidepoint((next_x,self.y)): #collide côté vx
                collide_vx = True
            elif wall.rect.collidepoint((self.x, self.y - vy//5)): #collide côté opposé vy
                collide_oppose_vy = True
            elif wall.rect.collidepoint((self.x - vx//5, self.y)): #collide côté opposé vx
                collide_oppose_vx = True
        
        if collide_vy:
            if not collide_vx:
                next_y = self.y
            else:
                if not collide_oppose_vy:
                    next_x = self.x
                    if abs(vx) > abs(vy) :
                        if vy > 0:
                            next_y = self.y - (5 * vy/vx)
                        else:
                            next_y = self.y + (5 * vy/vx)
                    elif abs(vy) >= abs(vx):
                        if vy > 0:
                            next_y = self.y - 5                    
                        else:
                            next_y = self.y + 5
                else:
                    next_y = self.y
                    if not collide_oppose_vx:
                        if abs(vx) >= abs(vy) :
                            if vx > 0:
                                next_x = self.x - 5
                            else:
                                next_x = self.x + 5
                        elif abs(vx) < abs(vy):
                            if vx > 0:
                                next_x = self.x - (5 * vx/vy) 
                            else:
                                next_x = self.x + (5 * vx/vy) 
                    else:
                        next_x = self.x
        else:
            if collide_vx:
                next_x = self.x 
                
        self.next_pos = (next_x,next_y)
        return (int(next_x),int(next_y))
                    
        
                    
                    
                
        

    def pathfiding(self,player,walls,ecran):        
        start = time.time()
        player_pos = (player.x//5,player.y//5)   #conversion de la position du joueur dans la matrice des positions possibles du mob 
         
        positions = np.zeros((800//5,1300//5)) #positions possibles 
        positions[self.y//5][self.x//5] = 1  

        nodes = [(self.x//5,self.y//5)]  
        continuer = True
        nodes_value = 2
        while continuer :
            next_nodes = []
            for node in nodes:
                x,y = node
                for yneighbor in [y-1,y,y+1]:
                    for xneighbor in [x-1,x,x+1]:
                        if positions[yneighbor][xneighbor] == 0:
                            if not collide_walls(walls,(xneighbor*5,yneighbor*5)):
                                #pygame.draw.rect(ecran,(255,255,255),pygame.rect.Rect((xneighbor*5,yneighbor*5)+(self.width,self.height)))
                                #pygame.display.update()
                                #ecran.fill((0,0,0))
                            
                                positions[yneighbor][xneighbor] = nodes_value
                                next_nodes.append((xneighbor,yneighbor))
                            if (xneighbor,yneighbor) == player_pos:
                                print("collide player")
                                continuer = False
                                ################################
                                #---Reconstruction du chemin---#
                                ################################
                                actual_node = (xneighbor,yneighbor)
                                node_number = nodes_value
                                while node_number != 2:
                                    i = actual_node[1]-1
                                    j = actual_node[0]-1
                                    while positions[i][j] != node_number -1:
                                        if j == actual_node[0] + 1:
                                            j = actual_node[0]-1
                                            i+=1
                                        else: j+=1
                                    node_number-=1
                                    actual_node = (j,i)
                                self.next_pos = (actual_node[0]*5,actual_node[1]*5)

            nodes_value += 1

            nodes = next_nodes



        

        """visites = []
        for i in range(800//5):
            ligne = []
            for j in range(1300//5):
                ligne.append(0)
            visites.append(ligne)

        visites[self.x//5][self.y//5] = 1



        while 1:               
            #print(len(self.chemin))
            next_chemin = []
            for chemin in self.chemin:
            
                #print(chemin)
            
                last_pos = chemin[-1]                
                
                neighbors = []
                for k in range(-5,6,5):
                    x = last_pos[0] + k
                    for j in range(-5,6,5):
                        y = last_pos[1] + j                    
                        if visites[x//5][y//5] == 0:
                            visites[x//5][y//5] = 1
                            neighbors.append((x,y))  
                            #print((x,y))



                for neighbor in neighbors:
                    if not self.collide(map_room,neighbor) and distance(neighbor,(player.x,player.y)) < distance(last_pos,(player.x,player.y))+2.5:                               
                        #pygame.draw.rect(ecran,(255,255,255),pygame.rect.Rect(neighbor+(self.width,self.height)))
                        #pygame.display.update()
                        next_chemin.append(self.chemin[0]+[neighbor])
                        if self.collide_player(player,neighbor):
                            self.chemin = self.chemin[-1][1:]
                            end = time.time()
                            print(end-start)
                            return True
            self.chemin = []
            for chemin in next_chemin:
                self.chemin.append(chemin)"""
            
            

                
        


    def collide_player(self,player,mob_pos):
        player_rect = pygame.rect.Rect(player.x,player.y,player.width,player.height)
        mob_rect = pygame.rect.Rect(mob_pos[0],mob_pos[1]+5,self.width,self.height)

        if mob_rect.colliderect(player_rect):
            return True 
        return False

    def collide(self,walls,neighbor):
        """retournes True si le mob collide avec un mur, sinon retournes False"""
        start = time.time()
        
        neighbor_rect = pygame.rect.Rect(neighbor[0],neighbor[1]+5,self.width,self.height)

        for wall in walls:
            if neighbor_rect.colliderect(wall.rect):
                return True
        return False
        



    def animate_death(self):
        self.death = True

    def update_death(self):
        if self.death:
            self.current_frame = self.death_frames[int(self.death_frame)]
            self.death_frame += 0.2
            if int(self.death_frame) == len(self.death_frames): #dernière frame deja utilisée
                self.dead = True
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



class Corpse:
    def __init__(self,id,init_x,init_y):
        self.id = id
        self.image = pygame.image.load("animations/death "+id+"/4.png")
        self.x = init_x
        self.y = init_y





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
    
    room_surface = pygame.Surface((19*taille_cases,21*taille_cases))
    path_to_map = "rooms/lobby/lobby"
    map = get_map_from_file(path_to_map)
    mobs,walls = create_room(room_surface,map)
    corpses = [] #liste des cadavres de mobs sur la map
    screen.blit(room_surface,(10,12))
   


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

        ###########################
        #---Monstre cible joueur--#
        ###########################
        for mob in mobs:
            start = time.time()
            if mob.ciblage(player,walls):
                end = time.time()
                print(end-start)
                print("monstre nb",mobs.index(mob)," peut cibler le joueur")

        
        ######################
        #---Pathfiding mob---#
        ######################
        """if mobs != []: 
            start = time.time()
            print("actual_pos : ",(mobs[0].x,mobs[0].y))
            new_pos = mobs[0].easy_pathfiding(player,walls)
            print("new pos : ",new_pos)
            print("player_pos :",(player.x,player.y))
            end = time.time()
            print(end-start)"""
        
                            
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



                if event.key == pygame.K_a: #lancement attaque joueur
                    player.start_attack()
                
                if event.key == pygame.K_SPACE:
                    if True in exits: #le personnage se trouve sur une des sorties
                        dungeon_pos,pos_player = change_room(dungeon,dungeon_pos,(player.x,player.y),exits)
                        player.update_pos(pos_player[0],pos_player[1])
                        map = dungeon[dungeon_pos] 
                        screen.fill((0,0,0))
                        mobs,walls = create_room(room_surface,map)
                        corpses = []
                         
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
            if mob.next_pos != ():
                new_pos = mob.next_pos
                mob.update_pos(new_pos[0],new_pos[1])
            if mob.death:
                mob.update_death()
            screen.blit(mob.current_frame,(mob.x,mob.y))

        #Gestion de l'attaque du joueur
        if player.attack == True:
            player.update_attack()
            if int(player.attack_frame) == 2:                
                for i in range(len(mobs)):
                    if player.collide_sword_mob(mobs[i]) and not player.dealt_dammages:  
                        player.dealt_dammages = True                      
                        mobs[i].take_dammage(player.atk)
                for mob in mobs:
                    if mob.dead == True:
                        corpses.append(Corpse(mob.id,mob.x,mob.y))
                        mobs.pop(mobs.index(mob))
                        #suppression du mob dans la map initiale du donjon, afin qu'il n'aparaisse plus si l'on revient dans la salle
                        line = map[mob.map_y]
                        new_line = line[:mob.map_x] + '_'+line[mob.map_x+1:]
                        map[mob.map_y] = new_line
                        dungeon[dungeon_pos] = map

        for corpse in corpses:
            screen.blit(corpse.image,(corpse.x,corpse.y))

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