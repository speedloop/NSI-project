import pygame

def get_map_from_file(path_to_file):
    with open(path_to_file,'r') as file:
        map = file.readlines()
        for i in range(len(map)):
            map[i] = map[i].rstrip('\n')
            print(map[i])
        file.close()
    return map

def display_room(screen,map_room):
    screen.fill((0,0,0))

    dict_textures = {
        '#': pygame.transform.scale(pygame.image.load("wall.png"),(37,37)),
        '.': pygame.transform.scale(pygame.image.load("empty.png"),(37,37)),
        '_': pygame.transform.scale(pygame.image.load("floor.png"),(37,37)),
        '@': pygame.transform.scale(pygame.image.load("spawner.png"),(37,37)),
        ':': pygame.transform.scale(pygame.image.load("floor.png"),(37,37))
    }

    for i in range(len(map_room)):
        for j in range(len(map_room[i])):
            screen.blit(dict_textures[map_room[i][j]], (37*j+10,37*i+12))


def game(screen):
    path_to_map = input("Entrer le chemin complet jusqu'au fichier contenant la salle à afficher : \n")
    map = get_map_from_file(path_to_map)

    

    continuer = True
    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    return True
        display_room(screen,map)
        pygame.display.update()



    return True






