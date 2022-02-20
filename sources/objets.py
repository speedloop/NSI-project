from random import randint
import pygame
from sources.constantes import *

# Dans ce fichier sont geres tous les objets qu'on peut retrouver dans le jeux. puis ce fichier est importe dans le game.py pour
# toutes les manipulations avec l'inventaire. Les vies sont egalement geres ici.

def viechange(v,vmax,prot,vchange):
    """Fonction qui permet calculer les vies apres une attaque. Prend en parametres: nombre de vie initial, nombre de vies max,
    la valeur defensive, et le changement de vie positif ou negatif"""
    if vchange<0:
        if vchange<prot:
            v+=vchange
    if vchange>0:
        if v+vchange<vmax:
            v+=vchange
        else:
            v=vmax
    return(v)





# Ceci est un dictionnaire de listes. Dans ce dictionnaire sont regroupes tous les objets qu'un joueur peut collecter dans 
# son inventaire. Chaque clef dans ce dictionnaire designe un objet. Cette clef est l'id de l'objet. Dans chaque liste, 
# est contenu tout le necessaire sur un objet dans l'ordre: id, nom de l'objet affiche, description, texture.
objets = {

"..." : ["...","...","...",icon_inventaire_vide], #rien
"health_small": ["health_small", "Small health potion", "A small health potion that restores 20 health", icon_health_small],    #petite potion de soin
"health_med": ["health_med","Medium health potion","A medium health potion that restores 50 heath ", icon_health_med],          #potion de soin moyenne
"health_big": ["health_big","Big health potion","A big health potion that restores 100 health", icon_health_big]                #grande potion de soin

}



def affichage_inventaire(inv,ecran):
    pygame.draw.rect(ecran,(255,255,255),(19*37+20,500, 1300-(19*37+24), 62),border_radius = 10)
    for i in range (9):
        rect_blit = (19*37+30+62*i,503)
        ecran.blit(inv[i][3],rect_blit)

def ajout_objet_inv(inv,ecran):
    """Fonction qui prends en parametre l'inventaire et la surface de l'ecran et gere l'ajout 
    d'un objet supplementaire dans l'inventaire, tire au sort automatiquement. Gere les surcharges d'inventaire aussi.
    retourne le nouvel inventaire"""

    #tirage au sort d'un item 
    d100 = int(randint(0,99))
    if d100 < 75:
        temp_slot = objets["health_small"]
    elif d100 < 90:
        temp_slot = objets["health_med"]
    else:
        temp_slot = objets["health_big"]
    
    for i in range(9):
        if inv[i] == objets["..."]: #case d'inventaire vide
            inv[i] = temp_slot
            temp_slot = objets["..."]
            break
    
    if temp_slot != objets["..."]: #inventaire déjà plein
        #affichage d'un écran pour sélectionner l'item à remplacer
        ecran.fill((0,0,0))
        annonce_font = tip_font
        annonce_titre = annonce_font.render("Your inventory is overloaded, please choose what to leave behind with the number buttons. What will remain in the center will be destroyed. When finished press Enter",1,(255,255,255))
        annonce_rect= (50,12,annonce_titre.get_width(),annonce_titre.get_height())                
        ecran.blit(annonce_titre,annonce_rect)
        pygame.draw.rect(ecran,(255,0,0),(180,130,96,76),border_radius = 10)
        temp_rect = (200,140)
        ecran.blit(temp_slot[3],temp_rect)

        pygame.draw.rect(ecran,(255,255,255),(40,40, 1300-(19*37+24), 62),border_radius = 10)
        #affichage des icones de chaque item de l'inventaire
        for i in range (9):
            rect_blit = (46+62*i,43)
            ecran.blit(inv[i][3],rect_blit)
        pygame.display.update()

        ecran_changement_inventaire = 0
        emergency_transition_slot = ""
        while ecran_changement_inventaire == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                            inv = False
                            ecran_changement_inventaire = 1
                            break
                if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_RETURN:
                            ecran_changement_inventaire = 1
                        if event.key == pygame.K_q:
                            ecran_changement_inventaire = 1
                            break
                        if event.key == pygame.K_1:
                            emergency_transition_slot = inv[0]
                            inv[0]= temp_slot
                            temp_slot = emergency_transition_slot
                        if event.key == pygame.K_2:
                            emergency_transition_slot = inv[1]
                            inv[1]= temp_slot
                            temp_slot = emergency_transition_slot
                        if event.key == pygame.K_3:
                            emergency_transition_slot = inv[2]
                            inv[2]= temp_slot
                            temp_slot = emergency_transition_slot
                        if event.key == pygame.K_4:
                                emergency_transition_slot = inv[3]
                                inv[3]= temp_slot
                                temp_slot = emergency_transition_slot
                        if event.key == pygame.K_5:
                                emergency_transition_slot = inv[4]
                                inv[4]= temp_slot
                                temp_slot = emergency_transition_slot
                        if event.key == pygame.K_6:
                                emergency_transition_slot = inv[5]
                                inv[5]= temp_slot
                                temp_slot = emergency_transition_slot
                        if event.key == pygame.K_7:
                                emergency_transition_slot = inv[6]
                                inv[6]= temp_slot
                                temp_slot = emergency_transition_slot
                        if event.key == pygame.K_8:
                                emergency_transition_slot = inv[7]
                                inv[7]= temp_slot
                                temp_slot = emergency_transition_slot
                        if event.key == pygame.K_9:
                                emergency_transition_slot = inv[8]
                                inv[8]= temp_slot
                                temp_slot = emergency_transition_slot

                        pygame.draw.rect(ecran,(255,255,255),(40,40, 1300-(19*37+24), 62),border_radius = 10)
                        for i in range (9):
                            icon_blit = (46+62*i,43)
                            ecran.blit(inv[i][3],icon_blit)
                        pygame.draw.rect(ecran,(255,0,0),(180,130,96,76),border_radius = 10)
                        temp_rect = (200,140)
                        ecran.blit(temp_slot[3],temp_rect)
                        pygame.display.update()
                        
    return (inv)

def consommation_objet(place_inv, vnc_func):
    objet_consomme = vnc_func["inventaire"][place_inv][0]
    if objet_consomme == "health_small": 
        vnc_func["vies"] = viechange(vnc_func["vies"],vnc_func["vies_max"],vnc_func["defense"],20)
    if objet_consomme == "health_med":
        vnc_func["vies"] = viechange(vnc_func["vies"],vnc_func["vies_max"],vnc_func["defense"],50)
    if objet_consomme == "health_big":
        vnc_func["vies"] = viechange(vnc_func["vies"],vnc_func["vies_max"],vnc_func["defense"],100)
    vnc_func["inventaire"][place_inv] = objets["..."]
    return (vnc_func)




