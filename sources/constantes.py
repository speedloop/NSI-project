import pygame,os


pygame.font.init()
#definition de constantes
taille_cases = 37     
hauteur_personnage = 30
largeur_personnage = 29
speed = 5
fps = 90

size_icon_setting = 60
marge_buttons_settings = 30

#definition de la taille d'une case de séléction de personnage (voir change_char.py) en fonction du nombre de personnages possibles
characters_img = os.listdir(os.getcwd()+'/characters')
nb_personnages = len(characters_img)
inter_pic = 12 #distance ente les photos des personnages
marge = 20
height_pic = ((800-marge) // (nb_personnages/2)) - inter_pic
width_pic = (1300/2) - (1.5*marge)

#definition de fonts
settings_done_button_font = pygame.font.Font("fonts/blantic.ttf",30)
tip_font = pygame.font.Font("fonts/optimus.ttf",36)
brush_font = pygame.font.Font("fonts/brush.ttf",40)
settings_buttons_font = pygame.font.Font("fonts/luna.ttf",20)
berp_font= pygame.font.Font("fonts/berp.ttf",40)

#correspondances entre les caracteres du fichier de la carte codifiée avec leur texture
dict_textures = {
    '#': pygame.transform.scale(pygame.image.load("textures/wall.png"),(taille_cases,taille_cases)),
    '.': pygame.transform.scale(pygame.image.load("textures/empty.png"),(taille_cases,taille_cases)),
    '_': pygame.transform.scale(pygame.image.load("textures/floor.png"),(taille_cases,taille_cases)),
    '@': pygame.transform.scale(pygame.image.load("textures/spawner.png"),(taille_cases,taille_cases)),
    ':': pygame.transform.scale(pygame.image.load("textures/floor.png"),(taille_cases,taille_cases)),
    '!': pygame.transform.scale(pygame.image.load("textures/floor.png"),(taille_cases,taille_cases)),
    '?': pygame.transform.scale(pygame.image.load("textures/chest.jpg"),(taille_cases,taille_cases)),
    '^': pygame.transform.scale(pygame.image.load("textures/open_chest.jpg"),(taille_cases,taille_cases))
}

#autres textures 
v = berp_font.render("1",1,(255,255,255))
heart = pygame.transform.scale(pygame.image.load("textures/heart.png"),(v.get_height(),v.get_height()))
settings_icon = pygame.transform.scale(pygame.image.load("textures/settings.png"),(size_icon_setting,size_icon_setting))
shield_icon = pygame.transform.scale(pygame.image.load("textures/shield.png"),(v.get_height(),v.get_height()))

#correspondances entre les caracteres du fichier du donjon codifié avec leur salle 
dict_salles = {
    '@':"rooms/lobby/",
    'x':"rooms/croisement/",
    'h':"rooms/horizontal/",
    'v':"rooms/vertical/",
    'z':"rooms/triple N-E-S/",
    's':"rooms/impasse entree sud/",
    'n':"rooms/impasse entree nord/",
    'e':"rooms/impasse entree est/",
    'o':"rooms/impasse entree ouest/",
    'p':"rooms/coin est sud/",
    'l':"rooms/coin nord est/",
    'j':"rooms/coin ouest nord/",
    'i':"rooms/coin sud ouest/",
    'c':"rooms/triple O-N-E/",
    'g':"rooms/triple S-O-N/",
    't':"rooms/triple O-S-E/",
    'f':"rooms/boss/"    
}

#definition de la surface du bonhomme de neige
mob_surf = pygame.transform.scale(pygame.image.load("mobs/snowman.png"),(32,37))

def constantes():
    global speed
    global taille_cases
    global hauteur_personnage
    global largeur_personnage
    global mob_surf
