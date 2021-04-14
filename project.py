from z3 import *
# USING Z3 WHICH IS AN *SMT SOLVER* NOT A SAT SOLVER 

# POSSIBILITY 1 (chosen) : 
#   define the different combinations of rotations and tiles
#   at the different positions

# POSSIBILITY 2 : define the tiles of top left, rop right, etc...
#   not as good as organizing them as arrays of tiles

# TR = [[Bool ('tile_%s_%s_topRight ' % (p, tn) for p in range(6))]
# TL = [[Bool ('tile_%s_%s_topLeft ' % (p, tn) for p in range(6))]
# BR = [[Bool ('tile_%s_%s_bottomRight ' % (p, tn) for p in range(6))]
# BL = [[Bool ('tile_%s_%s_bottomLeft ' % (p, tn) for p in range(6))]
# R = [[Bool ('tile_%s_%s_Right ' % (p, tn) for p in range(6))]
# L = [[Bool ('tile_%s_%s_Left ' % (p, tn) for p in range(6))]
#         for tn in range(6)]
# Rot = [[Int('tile_%s_%s_rotation ' % (r) )]]

# POSSIBILITY 3 : (proposed by Jason)
#sum of tile colors/numbers must be 6 + 5 ... 1
    #distinct
#SUM and DISTINCT constraint available

# r = 1
# o = 2
# y = 3
# g = 4
# b = 5
# p = 6

tile_1 = [  [1, 5, 4, 2, 6, 3], 
            [3, 1, 5, 4, 2, 6], 
            [6, 3, 1, 5, 4, 2],  
            [2, 6, 3, 1, 5, 4], 
            [4, 2, 6, 3, 1, 5], 
            [5, 4, 2, 6, 3, 1] ]
# shows all posible rotations of tile1

tile_2 = [  [1, 4, 5, 6, 2, 3],
            [3, 1, 4, 5, 6, 2],
            [2, 3, 1, 4, 5, 6],
            [6, 2, 3, 1, 4, 5],
            [5, 6, 2, 3, 1, 4],
            [4, 5, 6, 2, 3, 1] ]
# shows all posible rotations of tile2

tile_3 = [  [2, 6, 5, 1, 4, 3],
            [3, 2, 6, 5, 1, 4],
            [4, 3, 2, 6, 5, 1],
            [1, 4, 3, 2, 6, 5],
            [5, 1, 4, 3, 2, 6],
            [6, 5, 1, 4, 3, 2] ]
# shows all posible rotations of tile3

tile_4 = [  [2, 4, 5, 1, 6, 3],
            [3, 2, 4, 5, 1, 6], 
            [6, 3, 2, 4, 5, 1], 
            [1, 6, 3, 2, 4, 5], 
            [5, 1, 6, 3, 2, 4], 
            [4, 5, 1, 6, 3, 2] ]
# shows all posible rotations of tile4

tile_5 = [  [2, 6, 4, 1, 5, 3],
            [3, 2, 6, 4, 1, 5],
            [5, 3, 2, 6, 4, 1],
            [1, 5, 3, 2, 6, 4],
            [4, 1, 5, 3, 2, 6],
            [6, 4, 1, 5, 3, 2] ]
# shows all posible rotations of tile5

tile_6 = [  [6, 5, 1, 4, 2, 3],
            [3, 6, 5, 1, 4, 2],
            [2, 3, 6, 5, 1, 4],
            [4, 2, 3, 6, 5, 1],
            [1, 4, 2, 3, 6, 5],
            [5, 1, 4, 2, 3, 6] ]
# shows all posible rotations of tile6

tiles = [tile_1, tile_2, tile_3, tile_4, tile_5, tile_6]
# ^^ all of the tile options

# Condition : Colors matching at all sides
    #   Easiest to make different conditions for each tile that check the 
    #   needed adjacent tiles
# every position is assigned a tile

# tiles are setup using tiles[0-5][0-5]
    # with the first index being the choice of tile and the second being the rotation

# big question / problem : how to iterate through all of the tiles at each position
    # but at the same time so there is always 6 tiles on the board?
    # permutations ?? --> tried this but it does not work

a = Int('a')
b = Int('b')
c = Int('c')
d = Int('d')
e = Int('e')
f = Int('f')

ra = [Int(i) for i in range(6)]
rb = [Int(i) for i in range(6)]
rc = [Int(i) for i in range(6)]
rd = [Int(i) for i in range(6)]
re = [Int(i) for i in range(6)]
rf = [Int(i) for i in range(6)]

ind_c = (And [0 <= a < 6]
             [0 <= b < 6]
             [0 <= c < 6]
             [0 <= d < 6]
             [0 <= e < 6]
             [0 <= f < 6])

ind_all_c = (Sum(a, b, c, d, e, f) == 15)

# ^^ will give the index of which tile we are dealing with
#       in the tiles array 
# NOTE : this did not work because i guess permutations does not acutally give a list?


# a is the tile index for pos 0
# b is the tile index for pos 1
# c is the tile index for pos 2
# d is the tile index for pos 3
# e is the tile index for pos 4
# f is the tile index for pos 5

## The variable r needs to be replaced with something else to make this work
pos0_c = [[And ( ((tiles[ (tiles[a]) ][ra])[5] == (tiles[ (tiles[d]) ][rd])[2])
                ((tiles[ (tiles[a]) ][ra])[0] == (tiles[ (tiles[b]) ][rb])[3]))]
                for r in range(6)]
    #condition for the colors in position 0

pos1_c = [[And ( ((tiles[ (tiles[b]) ][rb])[5] == (tiles[ (tiles[e]) ][re])[2])
                ((tiles[ (tiles[b]) ][rb])[4] == (tiles[ (tiles[d]) ][rd])[1])
                ((tiles[ (tiles[b]) ][rb])[0] == (tiles[ (tiles[c]) ][rc])[3]))]
                 for r in range(6)]
    #condition for the colors in position 1

pos2_c = [[((tiles[ (tiles[c]) ][rc])[4] == (tiles[ (tiles[e]) ][re])[1])]
                 for r in range(6)]
    #condition for the colors in position 2

pos3_c = [[And ( ((tiles[ (tiles[d]) ][rd])[0] == (tiles[ (tiles[e]) ][re])[3])
                ((tiles[ (tiles[d]) ][rd])[5] == (tiles[ (tiles[f]) ][rf])[2]))]
                 for r in range(6)]
    #condition for the colors in position 3

pos4_c = [[((tiles[ (tiles[e]) ][re])[4] == (tiles[ (tiles[f]) ][rf])[1])]
                 for r in range(6)]
    #condition for the colors in position 4


#combine all of the constraints
thinkominous_c = ind_c + ind_all_c + pos0_c + pos1_c + pos2_c + pos3_c + pos4_c

#position
# Will be talking to Jason about this later 
instance = (...) #I dont know what the instance would be in this case ???

instance_c = [ If(instance)] # make the instance condition **still need to do this part

s = Solver()
s.add(thinkominous_c + instance_c) # put the two final conditions in the solver

if s.check() == sat:  #check if satisfiable
  m = s.model()
  r = [ [ m.evaluate( ** variable chosen ** ) for **ranges**]] # will replace these once the setup variables are figured out
  print_matrix(r) #prints out the solution

else
  print "failed to solve"

