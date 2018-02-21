#!/usr/bin/env python

#==============================================================================
# Please see readme for documentation
#==============================================================================

import sys
import cPickle
import timeit

def p(r,c):
    return [(r,c) for r,c in [(r-1,c),(r-1,c-1),(r-1,c+1),(r-2,c)] if in_board(r,c)] if r==6 else [(r,c) for r,c in [(r-1,c),(r-1,c-1),(r-1,c+1)] if in_board(r,c)]
def P(r,c):
    return [(r,c) for r,c in [(r+1,c),(r+1,c-1),(r+1,c+1),(r+2,c)] if in_board(r,c)] if r==1 else [(r,c) for r,c in [(r+1,c),(r+1,c-1),(r+1,c+1)] if in_board(r,c)]
def N(r, c):
    return [(r,c) for r,c in [(r+2,c-1),(r+2,c+1),(r+1,c-2),(r+1,c+2),(r-1,c-2),(r-1,c+2),(r-2,c-1),(r-2,c+1)] if in_board(r,c)]
def B(r, c):
    diff, summ = r-c, r+c
    return [(r,c) for r,c in filter(lambda a: a != (r, c), [(i, i-diff) for i in range(8)] + [(i, summ-i) for i in range(8)]) if in_board(r,c)]
def R(r, c):
    return [(r,c) for r,c in filter(lambda a: a != (r, c), [(r,i) for i in range(8)] + [(i,c) for i in range(8)]) if in_board(r,c)]
def Q(r, c):
    return R(r,c) + B(r,c)
def K(r, c):
    return [(r,c) for r,c in [(r+1,c+1),(r+1,c),(r+1,c-1),(r,c-1),(r-1,c-1),(r-1,c),(r-1,c+1),(r,c+1)] if in_board(r,c)]

def in_board(r, c):
    return 0 <= r <= 7 and 0 <= c <= 7

# row_n: next row, col_n: next col, row: current row, col: current col
# current location in string: r*8 + c
# next location in string: r_n*8 + c_n
def next_board(s, piece, r, c, r_n, c_n):
    s_prime = s[:r*8+c] + '.' + s[r*8+c + 1:]
    return s_prime[:r_n*8 + c_n] + piece + s_prime[r_n*8 + c_n+1:]

def loc(s, r, c):
    return s[r*8 + c]

def successor(s, t):
    if s in succ_dict:
        if t in succ_dict[s]:
            return succ_dict[s][t]
    board_list = []
    move_list = []
    f = [0, 0, 0]
    places_checked = set()
    global turn
    for i, piece in enumerate(s):
        r, c = i/8, i%8
        if piece in player[t]:
            f[0] += value[piece]*weight[0]
            possible_moves = possible_move[piece](r, c)
            # board_list.extend([next_board(s,piece,r,c,r_n,c_n) for r_n,c_n in possible_moves if is_valid(s,turn,piece,r,c,r_n,c_n)])
            boards = []
            for r_n, c_n in possible_moves:
                if is_valid(s, t, piece, r, c, r_n, c_n):
                    # boards.append(next_board(s, piece, r, c, r_n, c_n))
                    boards.append(to_queen(next_board(s,piece,r,c,r_n,c_n), turn))
                    move_list.append((piece, r, c, r_n, c_n))
                    f[1] += 1*weight[1]
                    places_checked.union((r_n, c_n))
            board_list.extend(boards)
        if turn == t:
            if piece in player[change_turn(t)]:
                f[0] -= value[piece]*weight[0]
                possible_moves = possible_move[piece](r, c)
                for r_n, c_n in possible_moves:
                    if is_valid(s, change_turn(t), piece, r, c, r_n, c_n):
                        f[1] -= 1*weight[1]
                        places_checked.difference((r_n, c_n))
    f[2] = len(places_checked)*weight[2]
    succ_dict[s] = {}
    succ_dict[s][t] = (board_list, move_list)
    if t == turn:
        cost_dict[s] = {}
        cost_dict[s][turn] = sum(f)
    return (board_list, move_list)

def to_queen(s, turn):
    if turn == 'w':
        for i, piece in enumerate(s[-8:]):
            if piece == 'P':
                s = s[:-8+i] + 'Q' + s[-7+i:]
    else:
        for i, piece in enumerate(s[:8]):
            if piece == 'p':
                s = s[:i] + 'q' + s[1+i:]
    return s

def is_valid(s, turn, piece, r, c, r_n, c_n):
    if turn=='w':
        if piece=='P': # Check the 'P' in advance
            if r_n-r==1 and c_n==c: # Check one-step move
                if loc(s,r_n,c_n) != '.':
                    return False
            elif r_n-r == 2: # Check the inital two-step move
                if r != 1:
                    return False
                elif loc(s,2,c) != '.':
                    return False
                elif loc(s,3,c) != '.':
                    return False
            elif c != c_n: # Check the attack move
                if loc(s,r_n,c_n) not in player['b']:
                    return False
        if loc(s,r_n,c_n) in player['w']:
            return False
    elif turn=='b':
        if piece=='p': # Check the 'P' in advance
            if r-r_n==1 and c_n==c: # Check one-step move
                if loc(s,r_n,c_n) != '.':
                    return False
            elif r-r_n == 2: # Check the inital two-step move
                if r != 6: # If not in the initial position, you can't make 2 step move
                    return False
                elif loc(s,4,c) != '.':
                    return False
                elif loc(s,5,c) != '.':
                    return False
            elif c != c_n: # Check the attack move
                if loc(s,r_n,c_n) not in player['w']:
                    return False
        if loc(s,r_n,c_n) in player['b']:
            return False

    if piece=='R' or piece=='Q' or piece=='r' or piece=='q':
        if r==r_n: # Horizontal move
            for i in range(min(c,c_n)+1, max(c,c_n)):
                if loc(s,r,i) != '.':
                    return False
        elif c==c_n: # Vertical move
            for i in range(min(r,r_n)+1, max(r,r_n)):
                if loc(s,i,c) != '.':
                    return False

    if piece=='B' or piece=='Q' or piece=='b' or piece=='q':
        if r-r_n == c-c_n: # RightDown or LeftUp
            for i in range(1, abs(c-c_n)):
                if loc(s,min(r,r_n)+i,min(c,c_n)+i) != '.':
                    return False
        elif r-r_n == c_n-c: # RightUp, LeftDown
            for i in range(1, abs(c-c_n)):
                if loc(s, max(r,r_n)-i, min(c,c_n)+i) != '.':
                    return False
    return True

#==============================================================================
# Calculate cost
def calculate_cost(s):
    # calculate f1,f2,f3 of the evaluation function
    try:
        return cost_dict[s][turn]
    except:
        f = [0,0,0]
        places_checked = set()
        for i, piece in enumerate(s):
            r, c = i/8, i%8
            if piece in player[turn]:
                f[0] += value[piece]*weight[0]
                possible_moves = possible_move[piece](r, c)
                for r_n,c_n in possible_moves:
                    if is_valid(s,turn,piece,r,c,r_n,c_n):
                        f[1] += 1*weight[1]
                        places_checked.union((r_n, c_n))
            if piece in player[change_turn(turn)]:
                f[0] -= value[piece]*weight[0]
                possible_moves = possible_move[piece](r, c)
                for r_n,c_n in possible_moves:
                    if is_valid(s,change_turn(turn),piece,r,c,r_n,c_n):
                        f[1] -= 1*weight[1]
                        places_checked.difference((r_n, c_n))
        f[2] = len(places_checked)*weight[2]
        return sum(f)

#==============================================================================
# Mini-Max with alpha beta pruning
def minimax_decision(s, t, h=3):
    s_p, m = successor(s, t)
    return max([(x[0], x[1], min_value(x[0],change_turn(t),h-1,float('-inf'),float('inf'))) for x in zip(s_p, m)], key = lambda item: item[2])[:2]
#    return max(map(lambda x: (x[0], x[1], min_value(x[0], turn, h, -inf, inf)), zip(s, m)), key = lambda k: k[2])[:2]

def max_value(s, t, h, alpha=float('-inf'), beta=float('inf')):
    if h == 0:
        return calculate_cost(s)
    if s in move_dict:
        if 'max' in move_dict[s]:
            return min_value(move_dict[s]['max'], change_turn(t), h-1, alpha, beta)
    best_child = None
    for s_prime in successor(s, t)[0]:
        val = min_value(s_prime, change_turn(t), h-1, alpha, beta)
        if alpha < val:
            alpha = val
            best_child = s_prime
        if alpha >= beta:
            move_dict[s] = {}
            move_dict[s]['max'] = best_child
            return alpha
    if best_child is not None:
        move_dict[s] = {}
        move_dict[s]['max'] = best_child
    return alpha
#    return max([min_value(s_prime, change_turn(t), h-1) for s_prime in successor(s, t)[0]])

def min_value(s, t, h, alpha=float('-inf'), beta=float('inf')):
    if h == 0:
        return calculate_cost(s)
    if s in move_dict:
        if 'min' in move_dict[s]:
            return max_value(move_dict[s]['min'], change_turn(t), h-1, alpha, beta)
    best_child = None
    for s_prime in successor(s, t)[0]:
        val = max_value(s_prime, change_turn(t), h-1, alpha, beta)
        if val < beta:
            beta = val
            best_child = s_prime
        if alpha >= beta:
            move_dict[s] = {}
            move_dict[s]['min'] = best_child
            return beta
    if best_child is not None:
        move_dict[s] = {}
        move_dict[s]['min'] = best_child
    return beta
#    return min([max_value(s_prime, change_turn(t), h-1) for s_prime in successor(s, t)[0]])

def change_turn(t):
    return "b" if t == "w" else "w"

def print_board(s):
    print "\n".join([" ".join(s[i:i+8]) for i in range(0,64,8)])

#######################################################################################
turn, S0, time_limit = sys.argv[1], sys.argv[2], float(sys.argv[3])
possible_move = {'K':K,'Q':Q,'R':R,'B':B,'N':N,'P':P,'k':K,'q':Q,'r':R,'b':B,'n':N,'p':p}
player = {'w':['K','Q','R','B','N','P'], 'b':['k','q','r','b','n','p']}
value = {'K':1000,'Q':9,'R':5,'B':3,'N':3,'P':1,'k':1000,'q':9,'r':5,'b':3,'n':3,'p':1}
name = {'K':"Kingfisher",'Q':"Quetzal",'R':"Robin",'B':"Blue jay",'N':"Nighthawk",'P':"Parakeet",
        'k':"kingfisher",'q':"quetzal",'r':"robin",'b':"blue jay",'n':"nighthawk",'p':"parakeet"}
weight = [10, 1, 2]

print "Thinking! Please wait...\n"
init_time = timeit.default_timer()
succ_dict = {}
cost_dict = {}
try:
    with open("move_dict.txt") as f:
        move_dict = cPickle.load(f)
except:
    move_dict = {}

S_next, M_next = minimax_decision(S0, turn, 1)
piece, r, c, r_n, c_n = M_next
print("Hmm, I'd recommend moving the {} at row {} column {} to row {} column {}.".format(name[piece],r+1,c+1,r_n+1,c_n+1))
print("New board:")
print(S_next)

h = 3
for i in range(3, 15, h):
    S_next, M_next = minimax_decision(S0, turn, i)
    piece, r, c, r_n, c_n = M_next
#    print "Hmm, I'd recommend moving the {} at row {} column {} to row {} column {}.\nNew board:\n{}".format(name[piece],r+1,c+1,r_n+1,c_n+1,S_next)
    print("Hmm, I'd recommend moving the {} at row {} column {} to row {} column {}.".format(name[piece],r+1,c+1,r_n+1,c_n+1))
    print("New board:")
    print(S_next)
    cPickle.dump(move_dict, open('move_dict.txt', 'w'))
    if timeit.default_timer() - init_time > time_limit:
        break
