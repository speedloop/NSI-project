import pygame

#definition de constantes

taille_cases = 37     
hauteur_personnage = 30
largeur_personnage = 29
speed = 5

#correspondances entre les caracteres du fichier de la carte codifiée avec leur texture
dict_textures = {
    '#': pygame.transform.scale(pygame.image.load("textures/wall.png"),(taille_cases,taille_cases)),
    '.': pygame.transform.scale(pygame.image.load("textures/empty.png"),(taille_cases,taille_cases)),
    '_': pygame.transform.scale(pygame.image.load("textures/floor.png"),(taille_cases,taille_cases)),
    '@': pygame.transform.scale(pygame.image.load("textures/spawner.png"),(taille_cases,taille_cases)),
    ':': pygame.transform.scale(pygame.image.load("textures/floor.png"),(taille_cases,taille_cases)),
    '!': pygame.transform.scale(pygame.image.load("textures/floor.png"),(taille_cases,taille_cases)),
    '?': pygame.transform.scale(pygame.image.load("textures/chest.jpg"),(taille_cases,taille_cases))
}

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
