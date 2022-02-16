import pygame
from sources.constantes import *

def change_char(screen):
    screen.fill((80,80,80))
    pygame.display.update()

    continuer = True
    while continuer :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        for i in range(2):
            for j in range(nb_personnages//2):
                case_rect = pygame.draw.rect(screen,(30,30,30),(marge+i*(marge+width_pic), marge+j*(inter_pic+height_pic) ,width_pic,height_pic))
                char_pic = pygame.transform.scale(pygame.image.load("characters/"+characters_img[j+(3*i)]),(largeur_personnage*int(min(height_pic,width_pic)//largeur_personnage),hauteur_personnage*int(min(height_pic,width_pic)//hauteur_personnage)))
                char_pic_pos = (case_rect[0] + case_rect[2]//2 - char_pic.get_width()//2 , case_rect[1] + case_rect[3]//2 - char_pic.get_height()//2)
                screen.blit(char_pic,char_pic_pos)
        pygame.display.update()

