# We create a piece
#This Piece holds a colour (white = 0 and black = 1) and a nature (pawn, king, queen,...)
class Piece:
    def __init__(self, couleur, nature):   
        self.couleur = couleur
        self.nature = nature

        
        
# Class pawn
class Pion:
    
    def __init__(self):
        # This is its name in the matrix
        self.nom = 'P'
        self.valeur = 1
    
    # Checks if a pawn has moved since the beginning of the game (used to check if the pawn can move forward two spots)
    def est_a_origine(self,y,couleur) :
        if (couleur == 1) and (y == 1) :
            return True
        elif (couleur == 0) and (y == 6) :
            return True
        else :
            return False

    # Defines all the movements that the pawn can do
    def deplacements(self,y,x,couleur,board):
        return self.deplacements_avant(y,x,couleur,board) + self.deplacements_diag_g(y,x,couleur,board) + self.deplacements_diag_d(y,x,couleur,board)
    
    
    
    # Test if the pawn can move forward
    def deplacements_avant(self,y,x,couleur,board):
        if ((couleur == 1) and (y == 7)) or ((couleur == 0) and (y == 0)):
            return []
        elif board.get_plateau()[y-1+2*couleur,x].piece == None :
            return [[y-1+2*couleur,x]] + self.deplacements_avant_double(y,x,couleur,board)
        else : 
            return []
    
    # Test if the conditions to move forward two spots are met.
    def deplacements_avant_double(self,y,x,couleur,board):
        if self.est_a_origine(y,couleur) and board.get_plateau()[y-2+4*couleur,x].piece == None :
            return [[y-2+4*couleur,x]]
        else :
            return []
        
    # Test if the conditions to move diagonally on the left are met.
    def deplacements_diag_g(self,y,x,couleur,board):
        if (x == 0) or ((couleur == 1) and (y == 7)) or ((couleur == 0) and (y == 0)):
            return []
        elif board.get_plateau()[y-1+2*couleur,x-1].piece == None :
            return []
        elif board.get_plateau()[y-1+2*couleur,x-1].piece.couleur == couleur :
            return []
        else :
            return [[y-1+2*couleur,x-1]]
    
    # Test if the conditions to movediagonally on the right  are met.
    def deplacements_diag_d(self,y,x,couleur,board):
        if (x == 7) or ((couleur == 1) and (y == 7)) or ((couleur == 0) and (y == 0)):
            return []
        elif board.get_plateau()[y-1+2*couleur,x+1].piece == None :
            return []
        elif board.get_plateau()[y-1+2*couleur,x+1].piece.couleur == couleur :
            return []
        else :
            return [[y-1+2*couleur,x+1]]
     
    
# Class Tower
class Tour:
    
    def __init__(self):
        # This is its name in the matrix
        self.nom = 'T'
        self.valeur = 5
        
     # Define all the movements that the tower can do
    def deplacements(self,y,x,couleur,board):
        return self.deplacements_haut(y,x,couleur,board) + self.deplacements_bas(y,x,couleur,board) + self.deplacements_gauche(y,x,couleur,board) + self.deplacements_droite(y,x,couleur,board)

    # Test if the tower can move up on the matrix and how many spots it can move, using recursivity.
    def deplacements_haut(self,y,x,couleur,board):
        if y == 0 :
            return []
        elif board.get_plateau()[y-1,x].piece == None :
            return [[y-1,x]] + self.deplacements_haut(y-1,x,couleur,board)
        elif board.get_plateau()[y-1,x].piece.couleur == couleur :
            return []
        else :
            return [[y-1,x]]
        
    # Test if the tower can move down on the matrix and how many spots it can move, using recursivity.
    def deplacements_bas(self,y,x,couleur,board):
        if y == 7 :
            return []
        elif board.get_plateau()[y+1,x].piece == None :
            return [[y+1,x]] + self.deplacements_bas(y+1,x,couleur,board)
        elif board.get_plateau()[y+1,x].piece.couleur == couleur :
            return []
        else :
            return [[y+1,x]]
    
    
    # Test if the tower can move right on the matrix and how many spots it can pass, using recursivity.
    def deplacements_droite(self,y,x,couleur,board):
        if x == 7 :
            return []
        elif board.get_plateau()[y,x+1].piece == None :
            return [[y,x+1]] + self.deplacements_droite(y,x+1,couleur,board)
        elif board.get_plateau()[y,x+1].piece.couleur == couleur :
            return []
        else :
            return [[y,x+1]]
     
    # Test if the tower can move left on the matrix and how many spots it can pass, using recursivity.
    def deplacements_gauche(self,y,x,couleur,board):
        if x == 0 :
            return []
        elif board.get_plateau()[y,x-1].piece == None :
            return [[y,x-1]] + self.deplacements_gauche(y,x-1,couleur,board)
        elif board.get_plateau()[y,x-1].piece.couleur == couleur :
            return []
        else :
            return [[y,x-1]]
        
# Class knight
        
class Cavalier:
    def __init__(self):
        
        # This is its name in the matrix
        self.nom = 'C'
        self.valeur = 5
    
    # Define all the movements that the knight can do
    def deplacements(self,y,x,couleur,board):
        D = []
        L = [[y+2,x+1],[y+2,x-1],[y-2,x+1],[y-2,x-1],[y+1,x+2],[y+1,x-2],[y-1,x+2,],[y-1,x-2]]
        for k in L :
            if (k[0] > 7) or (k[0] < 0) or (k[1] > 7) or (k[1] < 0) :
                pass
            elif board.get_plateau()[k[0],k[1]].piece == None :
                D += [k]
            elif board.get_plateau()[k[0],k[1]].piece.couleur != couleur :
                D += [k]
        return D
          
        
# Class bishop
class Fou:
    def __init__(self):
        # This is its name in the matrix
        self.nom = 'F'
        self.valeur = 5
    
     # Defines all the movements that the bishop can do
    def deplacements(self,y,x,couleur,board):
        return self.deplacements_h_g(y,x,couleur,board) + self.deplacements_h_d(y,x,couleur,board) + self.deplacements_b_g(y,x,couleur,board) + self.deplacements_b_d(y,x,couleur,board)
    
    # Tests if the conditions to move diagonally up left are met.
    def deplacements_h_g(self,y,x,couleur,board):
        if (y == 0) or (x == 0) :
            return []
        elif board.get_plateau()[y-1,x-1].piece == None :
            return [[y-1,x-1]] + self.deplacements_h_g(y-1,x-1,couleur,board)
        elif board.get_plateau()[y-1,x-1].piece.couleur == couleur :
            return []
        else :
            return [[y-1,x-1]]
    
    # Tests if the conditions to move diagonally up right are met.
    def deplacements_h_d(self,y,x,couleur,board):
        if (y == 0) or (x == 7):
            return []
        elif board.get_plateau()[y-1,x+1].piece == None :
            return [[y-1,x+1]] + self.deplacements_h_d(y-1,x+1,couleur,board)
        elif board.get_plateau()[y-1,x+1].piece.couleur == couleur :
            return []
        else :
            return [[y-1,x+1]]
    
    # Tests if the conditions to move diagonally down left are met.
    def deplacements_b_g(self,y,x,couleur,board):
        if (y == 7) or (x == 0) :
            return []
        elif board.get_plateau()[y+1,x-1].piece == None :
            return [[y+1,x-1]] + self.deplacements_b_g(y+1,x-1,couleur,board)
        elif board.get_plateau()[y+1,x-1].piece.couleur == couleur :
            return []
        else :
            return [[y+1,x-1]]
    
    # Tests if the conditions to move diagonally hight right are met.
    def deplacements_b_d(self,y,x,couleur,board):
        if (y == 7) or (x == 7):
            return []
        elif board.get_plateau()[y+1,x+1].piece == None :
            return [[y+1,x+1]] + self.deplacements_b_d(y+1,x+1,couleur,board)
        elif board.get_plateau()[y+1,x+1].piece.couleur == couleur :
            return []
        else :
            return [[y+1,x+1]]

#  Class queen
         
class Reine:
    def __init__(self):
        # This is its name in the matrix
        self.nom = 'Q'
        self.valeur = 12

    # Defines all the movements that the queen can do with the help of the bishop and tower's classes
    def deplacements(self,y,x,couleur,board):
         return (Fou().deplacements(y,x,couleur,board) + Tour().deplacements(y,x,couleur,board))
         
# Class king
    
class Roi:
    def __init__(self):
        # This is its name in the matrix
        self.nom = 'K'
        self.valeur = 1000

    # Defines all the movements that the king can do (it doesn't return the spots where same coloured pieces are)
    def deplacements(self,y,x,couleur,board):
        D = []
        for i in range(-1,2):
            for j in range(-1,2):
                pos_y, pos_x = y+i, x+j
                if (pos_y > 7) or (pos_y <0) or (pos_x > 7) or (pos_x < 0) :
                    pass
                elif board.get_plateau()[pos_y, pos_x].piece == None :
                    D += [[pos_y, pos_x]]
                elif board.get_plateau()[pos_y, pos_x].piece.couleur != couleur :
                    D += [[pos_y, pos_x]]
        return D
