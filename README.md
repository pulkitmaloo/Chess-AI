# Pichu (Simplified version of chess) playing AI agent

## Method: Minimax algorithm with alpha-beta search

### Evaluation Function

<a href="https://www.codecogs.com/eqnedit.php?latex=e(s)&space;=&space;\sum_{i=0}^2{&space;w_i&space;f_i}(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?e(s)&space;=&space;\sum_{i=0}^2{&space;w_i&space;f_i}(s)" title="e(s) = \sum_{i=0}^2{ w_i f_i}(s)" /></a>

where 

- <a href="https://www.codecogs.com/eqnedit.php?latex=f_0(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_0(s)" title="f_0(s)" /></a> = sum of value of pieces of MAX - sum of value of pieces of MIN
- <a href="https://www.codecogs.com/eqnedit.php?latex=f_1(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_1(s)" title="f_1(s)" /></a> = number of moves possible for MAX - number of moves possible for MIN
- <a href="https://www.codecogs.com/eqnedit.php?latex=f_2(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_2(s)" title="f_2(s)" /></a> = number of unique places in the board on which only MAX can attack in the next move

and

<a href="https://www.codecogs.com/eqnedit.php?latex=w&space;=&space;(10,1,2)&space;\in&space;R^3" target="_blank"><img src="https://latex.codecogs.com/gif.latex?w&space;=&space;(10,1,2)&space;\in&space;R^3" title="w = (10,1,2) \in R^3" /></a>

One interesting thing about `f[2]` is that, if say MAX's bishop can attack on (1,1) and MIN's bishop can also attack on (1,1) then it will be "0".
But if there's another MAX's piece that can attack on (1,1) then we will count that as "1"

- Value of each pieces on chess board
    - Parakeet - 1 point
    - Nighthawk - 3 points
    - Blue jay - 3 points
    - Robin - 5 points
    - Quetzal - 9 points
    - Kingfisher - 1,000 points

The fourth evaluation function that we wanted to implement was the Pawn Structure
    - For each pawn of MAX, +1 for each of MAX piece in the pawn's diagonal places

- The Algorithm 

We are using Mini-Max Algorithm with alpha beta pruning along with some additional features

- Our algorithm works in a Iterative Deepening Depth First Search fashion
- To make it work faster, we stored the successors of each state in a dictionary, so when we increase the max_depth of our algorithm        we can avoid finding successors again and again
- We also calculated the evaluation of a state while finding its successors and stored it in a dictionary. This way we were avoiding        looping through the board since we were already doing that while finding it's successors.
- We started our algorithm from height 3 which could be evaluated within a couple of seconds. So at first, we run minimax normally          and record for each state which is its 'max' successor or 'min' successor, we're storing this in a dictionary. 
- Now, for the second time we increment the height by 3, ie, now run to a depth 6. However, this time for the first max node we             evaluate all it's successor and for each successor onwards we just access its best child, ie, max node or min node. However,            after height 3, we haven't explored anything yet, so we explore again normally for all its successors using minimax with alpha          beta pruning to height and again store each node's best successor, ie, max or min node.  
- The algorithm keeps incrementing the height by 3 until the time ends.
- For each iteration of height, we also save our dictionary to a file which can used in the next time run of the program
    
    
- Other efforts
    - We experimented a lot with what height should we start from and how much we increase 
    - We also tried storing cost and succ dictionary to files however, it was huge and didn't work well as we expected

### Usage

You can run the program by following command:

```
$ ./pichu.py w RNBQKBNRPPPP.PPP............P......p............ppp.pppprnbqkbnr 3
```

Following is the output. The program suggests two moves in three seconds.

```
Thinking! Please wait...

Hmm, I'd recommend moving the Quetzal at row 1 column 4 to row 4 column 7.
New board:
RNB.KBNRPPPP.PPP............P.Q....p............ppp.pppprnbqkbnr
Hmm, I'd recommend moving the Blue jay at row 1 column 6 to row 5 column 2.
New board:
RNBQK.NRPPPP.PPP............P....B.p............ppp.pppprnbqkbnr
```

Here's are some more commands that show how the program works. `next` function is just used for this example (not used in `solve`).

Each of functions, Q, K, R, ... returns the possible moves of each piece in a board assumign the board is empty (row, col) 

If you run the program in interactive mode, you can check each of the functions.
```
$ python -i pichu.py w RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr 3
... above output 
>>> Q(0,0)
[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
>>> K(0,5)
[(1, 6), (1, 5), (1, 4), (0, 4), (0, 6)]
>>> R(1,1)
[(1, 0), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (0, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
>>> B(3,1)
[(2, 0), (4, 2), (5, 3), (6, 4), (7, 5), (0, 4), (1, 3), (2, 2), (4, 0)]
>>> N(5,5)
[(7, 4), (7, 6), (6, 3), (6, 7), (4, 3), (4, 7), (3, 4), (3, 6)]
>>> P(1,1)
[(2, 1), (2, 0), (2, 2), (3, 1)]
>>> p(6,1)
[(5, 1), (5, 0), (5, 2), (4, 1)]
```

If you look at `B(3,1)`, assuming that the board is empty, it returns all the possible moves of B in the board. Then, the algorithm figures out whether each move is valid or not. For the `P(1,1)` because it's at the starting position, there are two moves possible (2,1) and (3,1) if there's no piece in the position. If there's opponent piece in diagonal, it can take the piece in either position (2,0) or (2,2).

Following is the game played using this AI agent.

```
$ ~csb551/a2/client_pichu.sh ./pichu.py voltorb 5000
-> White (me) will be played by the local program called ./pichu.py
   Black will be played by remote program running on voltorb port 5000

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
RNBQKB.R
PPPPPPPP
.....N..
........
........
........
pppppppp
rnbqkbnr

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
RNBQKB.R
PPPPPPPP
.....N..
........
........
.p......
p.pppppp
rnbqkbnr

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
RNBQKB.R
P.PPPPPP
.....N..
.P......
........
.p......
p.pppppp
rnbqkbnr

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
RNBQKB.R
P.PPPPPP
.....N..
.P......
..p.....
.p......
p..ppppp
rnbqkbnr

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
RNBQKB.R
P.P.PPPP
.....N..
.P.P....
..p.....
.p......
p..ppppp
rnbqkbnr

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
RNBQKB.R
P.P.PPPP
.....N..
.PpP....
........
.p......
p..ppppp
rnbqkbnr

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
RN.QKB.R
P.P.PPPP
.....N..
.PpP....
......B.
.p......
p..ppppp
rnbqkbnr

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
RN.QKB.R
P.P.PPPP
.....N..
.PpP....
.p....B.
........
p..ppppp
rnbqkbnr

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
RN.QKB.R
P.P.PPPP
.....N..
.Pp.....
.p.P..B.
........
p..ppppp
rnbqkbnr

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
RN.QKB.R
P.P.PPPP
.....N..
.Pp.....
.p.P..B.
........
pb.ppppp
rn.qkbnr

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R..QKB.R
P.P.PPPP
..N..N..
.Pp.....
.p.P..B.
........
pb.ppppp
rn.qkbnr

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
R..QKB.R
P.P.PPPP
..N..N..
.Pp.....
.p.b..B.
........
p..ppppp
rn.qkbnr

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R...KB.R
P.P.PPPP
..N..N..
.Pp.....
.p.Q..B.
........
p..ppppp
rn.qkbnr

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
R...KB.R
P.P.PPPP
..N..N..
.Pp.....
.p.Q..B.
.....n..
p..ppppp
rn.qkb.r

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R...KB.R
P.P.PPPP
..N..N..
.Pp.....
.p....B.
.....n..
p..ppppp
Qn.qkb.r

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
R...KB.R
P.P.PPPP
..N..N..
.Pp.....
.p.n..B.
........
p..ppppp
Qn.qkb.r

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R...KB.R
P.P.PPPP
.....N..
.Pp.....
.p.N..B.
........
p..ppppp
Qn.qkb.r

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
R...KB.R
P.P.PPPP
.....N..
.Pp.....
.p.N..B.
........
p..ppppp
Qn.qkbr.

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R....B.R
P.PKPPPP
.....N..
.Pp.....
.p.N..B.
........
p..ppppp
Qn.qkbr.

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
R....B.R
P.PKPPPP
.....N..
.Pp.....
.p.N..B.
p.......
...ppppp
Qn.qkbr.

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R....B.R
P.PKPPPP
........
.Pp.....
.p.NN.B.
p.......
...ppppp
Qn.qkbr.

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
R....B.R
P.PKPPPP
........
.Pp.....
.p.NN.B.
p.......
..qppppp
Qn..kbr.

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R....B.R
P.PKPPPP
........
.Pp.....
.p..N.B.
p.......
..Nppppp
Qn..kbr.

-> Requesting move from other player...
-> Checking that move is valid...
-> New board state:
R....B.R
P.PKPPPP
........
.Pp.....
.p..N.Bp
p.......
..Npppp.
Qn..kbr.

-> White (me) thinking...
-> Checking that move is valid...
-> New board state:
R....B.R
P.PKPPPP
........
.Pp.....
.p..N.Bp
p.......
...pppp.
Qn..Nbr.

w WINS
```
