import pygame
from sources.constantes import *

def collide_mouse_case(cases_rects):
    for i in range(len(cases_rects)):
        if cases_rects[i].collidepoint(pygame.mouse.get_pos()): #la souris collide avec l'une des cases contenant l'image d'un personnage
            return i+1
    return False

def change_char(screen):
    cases_rects = []
    char_pics = []  #liste des imgaes de chaque personnage disponible

    continuer = True
    while continuer :        
        collide_case = collide_mouse_case(cases_rects)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if pygame.mouse.get_pressed()[0]: #seulement le click gauche
                if collide_case != False:
                    return characters_img[collide_case-1][:-4] #retourne le nom du fichier contenant l'image cliquée, sans son extension
                

        screen.fill((80,80,80))

        for i in range(3):
            for j in range(nb_personnages//3):
                case_rect = pygame.draw.rect(screen,(30,30,30),(marge+i*(marge+width_pic), marge+j*(inter_pic+height_pic) ,width_pic,height_pic))
                cases_rects.append(case_rect)
                char_pics.append(pygame.transform.scale(pygame.image.load("characters/"+characters_img[j+((nb_personnages//3)*i)]),(largeur_personnage*int(min(height_pic,width_pic)//largeur_personnage),hauteur_personnage*int(min(height_pic,width_pic)//hauteur_personnage))))
                char_pic_pos = (case_rect[0] + case_rect[2]//2 - char_pics[j+((nb_personnages//3)*i)].get_width()//2 , case_rect[1] + case_rect[3]//2 - char_pics[j+((nb_personnages//3)*i)].get_height()//2)
                screen.blit(char_pics[j+((nb_personnages//3)*i)],char_pic_pos)
        if collide_case != False:
            pygame.draw.rect(screen,(0,100,255),cases_rects[collide_case-1],2)

            
        pygame.display.update()

