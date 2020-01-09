
import copy
import pygame
import numpy as np
import time
import random
from Pieces import Piece
from Cases import Case
from Pieces import Piece,Pion,Cavalier,Fou,Tour,Roi,Reine

class Board:
    #le joueur jour toujours les blancs et se trouve en bas de l'ecran au debut
    def __init__(self):
        self.plateau = np.empty((8, 8), Case)
        self.couleur_jouee = 0
        self.piece_selectionnee = None
        self.case_selectionnee = None
        self.cases_selectionnables = []
        self.screen = pygame.display.set_mode((600,600))
        self.chess = pygame.image.load("chess.gif")
        self.echecB = pygame.image.load("echecB.gif")
        self.echecN = pygame.image.load("echecN.gif")
        self.changeN = pygame.image.load("changeN.gif")
        self.changeB = pygame.image.load("changeB.gif")
        self.position_rois = [[7,3],[0,3]]
        self.echec_et_maths = [False,None]
        self.rois_rock = [True,True]
        self.tours_rock = [[True,True],[True,True]]

    #getter
    def get_plateau(self):
        return self.plateau
  
    #on selectionne une case avec ses coordonnees
    def selectionner_case(self,y,x):
        if [y,x] in self.cases_selectionnables :
            self.get_plateau()[y,x].piece = self.piece_selectionnee
            self.get_plateau()[self.case_selectionnee[0],self.case_selectionnee[1]].piece = None
            if self.piece_selectionnee.nature.nom == 'K' :
                self.rois_rock[self.couleur_jouee] = False
                self.position_rois[self.piece_selectionnee.couleur] = [y,x]
                if abs(x-self.case_selectionnee[1]) == 2 :
                    self.tours_rock[self.couleur_jouee][self.case_selectionnee[1]//5] = False
                    self.get_plateau()[y,self.case_selectionnee[1]+ (x-self.case_selectionnee[1])//2].piece = Piece(self.couleur_jouee,Tour())
                    self.get_plateau()[y,(x//5)*7].piece = None
            if self.piece_selectionnee.nature.nom == 'T' and (self.tours_rock[self.couleur_jouee][self.case_selectionnee[1]//7] == True) :
                self.tours_rock[self.couleur_jouee][self.case_selectionnee[1]//7] = False
            if (self.piece_selectionnee.nature.nom == 'P') and (y == 7*self.couleur_jouee) :
                if self.couleur_jouee == 0:
                    self.display(self.changeB)
                else :
                    self.display(self.changeN)
                self.transformer_pion(y,x)
            self.couleur_jouee = 1 - self.couleur_jouee
            self.echec_maths()
            self.cases_selectionnables = []
            self.piece_selectionnee = None
            self.case_selectionnee = None

            
        elif self.get_plateau()[y,x].piece == None :
            pass
        
        elif self.get_plateau()[y,x].piece.couleur == self.couleur_jouee :
            self.piece_selectionnee = self.get_plateau()[y,x].piece
            self.case_selectionnee = [y,x]
            self.cases_selectionnables = self.verifie_echec(self.piece_selectionnee.nature.deplacements(y,x,self.couleur_jouee,self))
            if self.piece_selectionnee.nature.nom == 'K' :
                self.rock()

    def rock(self):
        c = self.couleur_jouee
        if self.rois_rock[c] and self.tours_rock[c][0] and (self.get_plateau()[7*(1-c),1].piece == None) and (self.get_plateau()[7*(1-c),2].piece == None) :
            self.cases_selectionnables += [[7*(1-c),1]]
        if self.rois_rock[c] and self.tours_rock[c][1] and (self.get_plateau()[7*(1-c),4].piece == None) and (self.get_plateau()[7*(1-c),5].piece == None) and (self.get_plateau()[7*(1-c),6].piece == None):
            self.cases_selectionnables += [[7*(1-c),5]]

            
    def transformer_pion(self,y,x):
        event = pygame.event.wait()
        while event.type != pygame.MOUSEBUTTONDOWN :
            event = pygame.event.wait()
        if event.pos[0] <= 300 and event.pos[1] >= 300:
            self.get_plateau()[y,x].piece = Piece(self.couleur_jouee,Cavalier())
        elif event.pos[0] <= 300 and event.pos[1] <= 300 :
            self.get_plateau()[y,x].piece = Piece(self.couleur_jouee,Tour())
        elif event.pos[0] >= 300 and event.pos[1] >= 300 :
            self.get_plateau()[y,x].piece = Piece(self.couleur_jouee,Fou())
        elif event.pos[0] >= 300 and event.pos[1] <= 300 :
            self.get_plateau()[y,x].piece = Piece(self.couleur_jouee,Reine())

    def display(self, changement = None):
        self.screen.fill((0,0,0))
        self.screen.blit(self.chess,(0,0))
        self.draw_cases_selectionnables(self.cases_selectionnables)
        for k in self.get_plateau():
            for case in k:
                if case.piece != None :
                    case.draw_piece(self)
        self.display_echec_et_maths()
        if changement != None :
            self.screen.blit(changement, (0,0))
        pygame.display.flip()

    def display_echec_et_maths(self):
        if (self.echec_et_maths[0] == True) and (self.echec_et_maths[1] == 0):
            self.screen.blit(self.echecB,(0,0))
        elif (self.echec_et_maths[0] == True) and (self.echec_et_maths[1] == 1):
            self.screen.blit(self.echecN,(0,0))

    def clic_to_case(self,pos):
        if (36 < pos[0]< 564) and (36 <= pos[1] <= 564):
            case_x = (pos[0]-36)//66
            case_y = (pos[1]-36)//66
            self.selectionner_case(case_y,case_x)

    def draw_cases_selectionnables(self, cases_a_colorier):
        for case in cases_a_colorier :
            pygame.draw.rect(self.screen, (0,255,0), [case[1]*66+36, case[0]*66+36, 66, 66])

    def verifie_echec(self, liste_cases):
        Liste_possible = []
        for case in liste_cases :
            board_copie = self.copier()
            board_copie.get_plateau()[case[0], case[1]].piece = self.piece_selectionnee
            board_copie.get_plateau()[self.case_selectionnee[0], self.case_selectionnee[1]].piece = None
            if board_copie.get_plateau()[case[0],case[1]].piece.nature.nom == 'K':
                board_copie.position_rois[self.couleur_jouee] = [case[0],case[1]]
            else :
                board_copie.position_rois = self.position_rois*1
            if board_copie.roi_en_echec(self.couleur_jouee) == False:
                Liste_possible += [case]
        return Liste_possible

    def roi_en_echec(self, couleur):
        for i in range(8):
            for j in range(8):
                if self.get_plateau()[i,j].piece == None :
                    pass
                elif (self.get_plateau()[i,j].piece.couleur == 1-couleur) and (self.position_rois[couleur] in self.get_plateau()[i,j].piece.nature.deplacements(i,j,1-couleur,self)) :
                    return True
        return False

    def echec_maths(self):
        for i in range(8):
            for j in range(8):
                if (self.get_plateau()[i,j].piece == None):
                    pass
                elif self.get_plateau()[i,j].piece.couleur == self.couleur_jouee :
                    self.piece_selectionnee = self.get_plateau()[i,j].piece
                    self.case_selectionnee = [i,j]
                    self.cases_selectionnables = self.verifie_echec(self.piece_selectionnee.nature.deplacements(i,j,self.couleur_jouee,self))
                    if (self.cases_selectionnables != []):
                        return False
        self.echec_et_maths = [True, self.couleur_jouee]
        return True

    def copier(self):
        copie = Board()
        for i in range(8):
            for j in range(8):
                copie.plateau[i,j] = Case(i,j,self.get_plateau()[i,j].piece)
        return copie

    def ia2(self,liste = None, limite = 1000):
        if liste == None :
            couleur = self.couleur_jouee
            liste_case = []
            for i in range(8):
                for j in range(8):
                    liste_case += [[i,j]]
            random.shuffle(liste_case)
        else :
            couleur = 1 - self.couleur_jouee
            liste_case = liste
        valeur_deplacement = -1000
        depart = [None,None]
        arrivee = [None,None]
        for k in liste_case :
            liste_deplacements = []
            if self.get_plateau()[k[0],k[1]].piece == None:
                pass
            elif self.get_plateau()[k[0],k[1]].piece.couleur == couleur:
                self.case_selectionnee = [k[0],k[1]]
                self.piece_selectionnee = self.get_plateau()[k[0],k[1]].piece
                liste_deplacements = self.verifie_echec(self.piece_selectionnee.nature.deplacements(k[0],k[1],couleur,self))
                if liste == None :
                    random.shuffle(liste_deplacements)
            for d in liste_deplacements :
                self.piece_selectionnee = self.get_plateau()[k[0],k[1]].piece
                valeur1 = self.give_valeur_deplacement_tour1(d)
                if valeur1 >= limite :
                    return 1000
                if valeur1 >= valeur_deplacement and liste != None :
                    valeur_deplacement = valeur1
                if valeur1 > valeur_deplacement and liste == None :
                    board_copie = self.copier()
                    board_copie.get_plateau()[d[0], d[1]].piece = self.piece_selectionnee
                    board_copie.get_plateau()[k[0], k[1]].piece = None
                    valeur2 = valeur1 - board_copie.ia2(liste_case,valeur1 - valeur_deplacement)
                    if valeur2 > valeur_deplacement:
                        valeur_deplacement = valeur2
                        depart = k
                        arrivee = d
        if liste == None :
            self.selectionner_case(depart[0],depart[1])
            self.display()
            time.sleep(0.5)
            self.selectionner_case(arrivee[0],arrivee[1])
        return (valeur_deplacement)

    def give_valeur_deplacement_tour1(self,d):
        if self.get_plateau()[d[0],d[1]].piece == None :
            return 0
        return self.get_plateau()[d[0],d[1]].piece.nature.valeur

    def ia(self):
        liste_case = []
        for i in range(8):
                for j in range(8):
                    liste_case += [[i,j]]
        random.shuffle(liste_case)
        valeur_deplacement = -1000
        depart = [None,None]
        arrivee = [None,None]
        for k in liste_case :
            if self.get_plateau()[k[0],k[1]].piece == None:
                liste_deplacements = []
            elif self.get_plateau()[k[0],k[1]].piece.couleur == self.couleur_jouee:
                self.case_selectionnee = [k[0],k[1]]
                self.piece_selectionnee = self.get_plateau()[k[0],k[1]].piece
                liste_deplacements = self.verifie_echec(self.piece_selectionnee.nature.deplacements(k[0],k[1],self.couleur_jouee,self))
            for d in liste_deplacements:
                valeur = 0
                if self.get_plateau()[d[0],d[1]].piece == None :
                    pass
                elif self.get_plateau()[d[0],d[1]].piece.couleur == 1 - self.couleur_jouee :
                    valeur = self.get_plateau()[d[0],d[1]].piece.nature.valeur

       
