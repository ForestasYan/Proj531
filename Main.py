
import pygame
from Board import Board
from Cases import Case
from Pieces import Piece,Pion,Cavalier,Fou,Tour,Roi,Reine
menu = pygame.image.load("menu.gif")

def main() :
    #on cree un board qui est un tableau numpy compose de zeros
    board = Board()

    pygame.init()


    #placement des cases vides
    for i in range(2,6):
       for j in range(8):
            board.plateau[i,j] = Case(i,j, None)
    

    #placement des pions
    for i in range(8):
        board.plateau[6,i] = Case(6,i, Piece(0, Pion()))
        board.plateau[1,i] = Case(1,i, Piece(1, Pion()))
    

    #placement des tours
    for i in [0,7] :
        board.plateau[0,i] = Case(0,i,Piece(1,Tour()))
        board.plateau[7,i] = Case(7,i,Piece(0,Tour()))
    
    #placement des cavaliers
    for i in [1,6] :
        board.plateau[0,i] = Case(0,i,Piece(1,Cavalier()))
        board.plateau[7,i] = Case(7,i,Piece(0,Cavalier()))
    
    #placement des fous
    for i in [2,5] :
        board.plateau[0,i] = Case(0,i,Piece(1,Fou()))
        board.plateau[7,i] = Case(7,i,Piece(0,Fou()))
    
    #placement des reines
    board.plateau[0,4] = Case(0,4,Piece(1,Reine()))
    board.plateau[7,4] = Case(7,4,Piece(0,Reine()))
    
    
    #placement des rois
    board.plateau[0,3] = Case(0,3,Piece(1,Roi()))
    board.plateau[7,3] = Case(7,3,Piece(0,Roi()))

    

    # Infinite loop    
    while True:
    
        event = pygame.event.wait()
 
        if event.type == pygame.QUIT:
            pygame.quit()
            break 
        if board.menu == False :
            board.display_menu()
        else :
            board.display()

        if board.jouer_ia == True :

            if event.type == pygame.MOUSEBUTTONDOWN and board.couleur_jouee == 0:
                board.clic_to_case(event.pos)

            elif board.couleur_jouee == 1 :
                board.ia()

        else :
            
            if event.type == pygame.MOUSEBUTTONDOWN :
                board.clic_to_case(event.pos)
            


        
# Calls the main function
if __name__ == "__main__":
    main()    




