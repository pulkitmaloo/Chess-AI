#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 08 10:14:39 2017
@author: PulkitMaloo
"""

import sys

class Board(object):
    def __init__(self, board):
        self.board = board
    def __str__(self): return "\n".join([" ".join(self.board[i:i+8]) for i in range(0,64,8)])
    def succ(self, player="w"):
        succ_list = []
        player_piece_check = {"w":"isupper", "b":"islower"}
        pieces_dict = {"P":"parakeet", "Q":"quetzal", "B":"bluejay", "N":"nighthawk", "R":"robin", "K":"kingﬁsher"}
        for i, piece in enumerate(self.board):
            if eval("piece."+player_piece_check[player]+"()"):
                try:
                    print("self.move_"+pieces_dict[piece.upper()]+"("+str(i)+")")
                    succ_list.extend(eval("self.move_"+pieces_dict[piece.upper()]+"("+str(i)+")"))
                except:
                    pass
        return succ_list
    def move_parakeet(self, i, player = "w"):
        succ = []
        if player == "w":
            if self.board[i+8] == ".":
                if i+8 >= 48:
                    pass
#                        succ.append()      # <- convert to quetzel
                else:
                    succ.append(self.move_vertical_down(i))
                    if 8 <= i <= 15 and self.board[i+16] == ".":
                        succ.append(self.move_vertical_down(i+8))
#                if self.board[i+7] != ".":

        else:
            if self.board[i-8] == ".":
                succ.append(self.move_vertical_up(i))
        return succ

    def move_vertical_down(self, i):
        b = list(self.board)
        b[i], b[i+8] = b[i+8], b[i]
        return Board(''.join(b))
#        return Board(self.board[:i]+"."+self.board[i+1:i+8]+self.board[i]+self.board[i+9:])
    def move_vertical_up(self, i):
        b = list(self.board)
        b[i], b[i-8] = b[i-8], b[i]
        return Board(''.join(b))
    def move_diagonal_up_right(self,i):
        b = list(self.board)
        b[i], b[i-7] = b[i-7], b[i]
        return Board(''.join(b))
    def move_diagonal_up_left(self,i):
        b = list(self.board)
        b[i], b[i-9] = b[i-9], b[i]
        return Board(''.join(b))
    def move_diagonal_down_right(self,i):
        b = list(self.board)
        b[i], b[i+9] = b[i+9], b[i]
        return Board(''.join(b))
    def move_diagonal_down_left(self,i):
        b = list(self.board)
        b[i], b[i+7] = b[i+7], b[i]
        return Board(''.join(b))

try:
    curr_player = sys.argv[1]
    initial_board = sys.argv[2]
    time = sys.argv[3]
except:
    curr_player = "w"
    initial_board = "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"
    time = 10

b = Board(initial_board)
for i in b.succ():
    print i