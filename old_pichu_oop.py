#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 08 10:14:39 2017
@author: PulkitMaloo
"""
##Can use signal or resource module to stop the program

import sys
from copy import deepcopy

class Piece(object):
    def __init__(self, x=None, y=None, p=None):
        self.position_x = x
        self.position_y = y
        self.piece_type = None
        self.player = None if p == "." else "w" if p.isupper() else "b"
    def __str__(self): return "."
    def getPosition(self): return self.position_x, self.position_y
    def setPosition(self, x, y):
        self.position_x = x
        self.position_y = y

class Parakeet(Piece):
    def __init__(self, x=None, y=None, p=None):
        Piece.__init__(self, x, y, p)
        self.piece_type = "Parakeet"
        self.first_move = True
    def __str__(self): return "P" if self.player == "w" else "p"

class Robin(Piece):
    def __init__(self, x=None, y=None, p=None):
        Piece.__init__(self, x, y, p)
        self.piece_type = "Robin"
    def __str__(self): return "R" if self.player == "w" else "r"

class Bluejay(Piece):
    def __init__(self, x=None, y=None, p=None):
        Piece.__init__(self, x, y, p)
        self.piece_type = "Bluejay"
    def __str__(self): return "B" if self.player == "w" else "b"

class Quetzal(Piece):
    def __init__(self, x=None, y=None, p=None):
        Piece.__init__(self, x, y, p)
        self.piece_type = "Quetzal"
    def __str__(self): return "Q" if self.player == "w" else "q"

class Nighthawk(Piece):
    def __init__(self, x=None, y=None, p=None):
        Piece.__init__(self, x, y, p)
        self.piece_type = "Nighthawk"
    def __str__(self): return "N" if self.player == "w" else "n"

class Kingfisher(Piece):
    def __init__(self,x=None,y=None,p=None):
        Piece.__init__(self, x, y, p)
        self.piece_type = "Kingfisher"
    def __str__(self): return "K" if self.player == "w" else "k"
    def getPosition(self): return self.position_x, self.position_y


class Board(object):
    def __init__(self, board):
        self.board = board if isinstance(board, list) else self.create_board(board)
    def __repr__(self):
        return "\n".join([" ".join([str(self.board[i][j]) for j in range(8)]) for i in range(8)])
    def create_board(self, init_board):
        pieces_dict = {"P":"Parakeet", "Q":"Quetzal", "B":"Bluejay", "N":"Nighthawk", "R":"Robin", "K":"Kingfisher", "p":"Parakeet", "q":"Quetzal", "b":"Bluejay", "n":"Nighthawk", "r":"Robin", "k":"Kingfisher", ".":"Piece"}
        board = [[None]*8 for i in range(8)]
        for i, piece in enumerate(init_board):
            x, y = i/8, i%8
            board[x][y] = eval(pieces_dict[piece]+"("+str(x)+","+str(y)+","+"'"+str(piece)+"'"+")")
        return board
    def __getitem__(self, indices):
#        if not isinstance(indices, tuple):
#            indices = tuple(indices)
        return self.board[indices]
        def heuristic(self, board): pass

class Player(object):
    def __init__(self, name, board):
        self.name = name
        self.turn = False
        self.player_pieces = self.getPieces(board)
    def getPieces(self, board):
        player_pieces = []
        for row in board:
            for piece in row:
                if piece.player == self.name:
                    player_pieces.append(piece)
        return player_pieces
    def removePiece(self, piece):
        self.player_pieces.remove(piece)
    def move_piece(self, board, piece): pass
    def possible_moves(self, board):
        moves = []
        for piece in self.player_pieces:
            moves.append(eval("self.move_"+piece.piece_type.lower()+"(board, piece)"))
        return moves
    def shift_move(self, board, from_x, from_y, to_x, to_y):
        board[from_x][from_y].setPosition(to_x, to_y)
        board[from_x][from_y], board[to_x][to_y] = board[to_x][to_y], board[from_x][from_y]
        return board
    def kill_move(self, board, from_x, from_y, to_x, to_y):
#        self.removePiece(board[to_x][to_y])
        board[from_x][from_y].setPosition(to_x, to_y)
        board[to_x][to_y] = board[from_x][from_y]
        board[from_x][from_y] = Piece(from_x, from_y, ".")
        return board
    def isMoveValid(self, board, from_x, from_y, to_x, to_y):
        if 0 <= to_x <= 7 and 0 <= to_y <= 7:
            if board[to_x][to_y].piece_type:
                return "kill" if board[to_x][to_y].player != board[from_x][from_y].player else False
            return "shift"
        return False
    def canMoveDown(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x+1, y)
    def canMoveUp(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x-1, y)
    def canMoveRight(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x, y+1)
    def canMoveLeft(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x, y-1)
    def canMoveUpRight(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x-1, y+1)
    def canMoveDownRight(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x+1, y+1)
    def canMoveDownLeft(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x+1, y-1)
    def canMoveUpLeft(self, board, piece):
        x, y = piece.getPosition()
        return self.isMoveValid(board, x, y, x-1, y-1)
    def move_kingfisher(self, board, piece):
        moves = []
        x, y = piece.getPosition()
        moves_direction = {'Down':("x+1","y"),'Up':("x-1","y"),'Right':("x","y+1"),'Left':("x","y-1"),'UpRight':("x-1","y+1"),'DownRight':("x+1","y+1"),'DownLeft':("x+1","y-1"),'UpLeft':("x-1","y-1")}
        for direction in moves_direction:
            move_type = eval("self.canMove"+direction+"(board, piece)")
            if move_type:
                moves.append(eval("self."+move_type+"_move(deepcopy(board), x, y, "+moves_direction[direction][0]+","+moves_direction[direction][1]+")"))
        return moves
    def move_quetzel(self, board, piece):
        moves = []
        x, y = piece.getPosition()
        return moves

    def move_parakeet(self, board, piece):
        moves = []
        x, y = piece.getPosition()
        if self.name == "w":
            if x+1 <= 7:
                #move down if no blocking
                if not board[x+1][y].piece_type:
                    moves.append(self.shift_move(board, x, y, x+1, y))
                    if piece.first_move and not board[x+2][y].piece_type:
                        moves.append(self.shift_move(board, x, y, x+2, y))
                if board[x+1][y+1].piece_type != piece.piece_type:
                    moves.append(self.kill_move(board, x, y, x+1, y+1))
                if board[x+1][y-1].piece_type != piece.piece_type:
                    moves.append(self.kill_move(board, x, y, x+1, y-1))
#                piece.first_move = False #<- when actual move will be made
                if x+1 == 7:
                    #convert to queen
                    pass
        else:
            if x-1 >= 0:
                if not board[x-1][y].piece_type:
                    moves.append(self.shift_move(board, x, y, x-1, y))
                    if piece.first_move() and not board[x-2][y].piece_type:
                        moves.append(self.shift_move(board, x, y, x-2, y))
                if board[x-1][y+1].piece_type != piece.piece_type:
                    moves.append(self.kill_move(board, x, y, x-1, y+1))
                if board[x-1][y-1].piece_type != piece.piece_type:
                    moves.append(self.kill_move(board, x, y, x-1, y-1))
        return moves

    def move_robin(self, board, piece):
        moves = []
        return moves

    def move_bluejay(self, board, piece):
        moves = []
        return moves

def move_up(board, piece):
    x = piece.position_x
    y = piece.position_y
    if board[x-1][y].piece_type:
        board[x][y], board[x-1][y] = board[x-1][y], board[x][y]
        piece.position_x -= 1
    elif board[x-1][y].player != piece.player:
        board[x][y] = Piece(x, y, ".")
        board[x-1][y] = piece
        piece.position_x -= 1
    else:
        pass
    return board

def move_right(board, piece):
    x = piece.position_x
    y = piece.position_y
    if board[x][y+1].piece_type:
        board[x][y], board[x][y+1] = board[x][y+1], board[x][y]
        piece.position_y += 1
    elif board[x][y+1].player != piece.player:
        board[x][y] = Piece(x, y, ".")
        board[x][y+1] = piece
        piece.position_y += 1
    else:
        pass
    return board

def move_left(board, piece):
    x = piece.position_x
    y = piece.position_y
    if board[x][y-1].piece_type:
        board[x][y], board[x][y-1] = board[x][y-1], board[x][y]
        piece.position_y -= 1
    elif board[x][y-1].player != piece.player:
        board[x][y] = Piece(x, y, ".")
        board[x][y-1] = piece
        piece.position_y -= 1
    else:
        pass
    return board

def move_up_right(board, piece):
    x = piece.position_x
    y = piece.position_y
    if board[x-1][y+1].piece_type:
        board[x][y], board[x-1][y+1] = board[x-1][y+1], board[x][y]
        piece.position_x -= 1
        piece.position_y += 1
    elif board[x-1][y+1].player != piece.player:
        board[x][y] = Piece(x, y, ".")
        board[x-1][y+1] = piece
        piece.position_x -= 1
        piece.position_y += 1
    else:
        pass
    return board

def move_up_left(board, piece):
    x = piece.position_x
    y = piece.position_y
    if board[x-1][y-1].piece_type:
        board[x][y], board[x-1][y-1] = board[x-1][y-1], board[x][y]
        piece.position_x -= 1
        piece.position_y -= 1
    elif board[x-1][y-1].player != piece.player:
        board[x][y] = Piece(x, y, ".")
        board[x-1][y-1] = piece
        piece.position_x -= 1
        piece.position_y -= 1
    else:
        pass
    return board

def move_down_right(board, piece):
    x = piece.position_x
    y = piece.position_y
    if board[x+1][y+1].piece_type:
        board[x][y], board[x+1][y+1] = board[x+1][y+1], board[x][y]
        piece.position_x += 1
        piece.position_y += 1
    elif board[x+1][y+1].player != piece.player:
        board[x][y] = Piece(x, y, ".")
        board[x+1][y+1] = piece
        piece.position_x += 1
        piece.position_y += 1
    else:
        pass
    return Board(board)

def move_down_left(board, piece):
    x = piece.position_x
    y = piece.position_y
    if board[x+1][y-1].piece_type:
        board[x][y], board[x+1][y-1] = board[x+1][y-1], board[x][y]
        piece.position_x += 1
        piece.position_y -= 1
    elif board[x+1][y-1].player != piece.player:
        board[x][y] = Piece(x, y, ".")
        board[x+1][y-1] = piece
        piece.position_x += 1
        piece.position_y -= 1
    else:
        pass
    return board




class Game(object):
    def __init__(self): pass

if __name__ == "__main__":
    try:
        curr_player = sys.argv[1]
        initial_board = sys.argv[2]
        time = sys.argv[3]
    except:
        curr_player = "w"
        initial_board = "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"
        time = 10

    b = Board(initial_board)
    print b
#    move_down_right(b.board, b[1][4])
    W = Player("w", b.board)
    i = W.move_parakeet(b.board,b[1][4])
    for x in i:
        print Board(x)
