from z3 import *

## Game plan : make separate positions for each of the rotations
#   so that when we implement it, it we do not have to go through a
#   big list to access the rotations - we just get the positions

# note: the tests that are used in this program are just print statements
#       because the normal testing method for python does not work on 
#       z3 because they do not resolve to boolean values or real values
#       that can be compared. This is why I decided to use print statements 
#       that describe what the printed value should look like (I chose to
#       describe the output rather than printing what it should be, because
#       there are too many values, so it would be very messy looking)

num_tiles = 6
tile_sides = 6
colors = 6

# the positions of the tiles -> the index represents which tile
tile_pos =  [ Int("Position of tile %s" % (i+1)) for i in range(num_tiles) ]

# Kind of a test: check to see if tile_pos is the correct result
print("Check equal:\n", tile_pos, "\n [Position of tile 1, Position of tile 2, Position of tile 3, Position of tile 4, Position of tile 5, Position of tile 6]\n") 

# the colors of the positions on the board -> the index represents the board position
board_pos = [ Int("Board position_%s" % i) for i in range(num_tiles * tile_sides)]

# Kind of a test: check to see if board_pos is the correct result
print("Check equal:\n", board_pos, "\n *These should be a list of labeled values ranging from 0 to 35\n")

# every board position has 1 of 6 colors so their values can only be 1-6
board_pos_constraints = [And(1 <= board_pos[i], board_pos[i] <= colors) for i in range(num_tiles * tile_sides)]

# every tile is in position 1 through 6
tile_constraints = [And(1 <= tile_pos[i], tile_pos[i] <= num_tiles) for i in range(num_tiles)]

#testing that the board and tile positions are less than 6 and greater than 1
print("Check equal:\n", board_pos_constraints, "\n", tile_constraints, 
        "\n *This should print two lists that compare all of the values for the positions with the range of values [1-6]\n")

# tiles must be in different locations on the board (no overlapping)
no_two_same_place = [ Distinct(tile_constraints) ]

# I will not do a test for this because it is just taking the results from the tile constraints and making sure that they
# are all unique

# tiles have only one of each color (no repeats)
no_two_face_same_color = [ Distinct(board_pos[((i * tile_sides)+1):((i * tile_sides) + tile_sides)])
                           for i in range(num_tiles)]

# I will not do a test for this because it is just taking each "grouping" of the board positions and making sure they are 
# all different
            
# these are the 6 tile options - specific to the given colored tiles
# will place these values throughout 
instance = [[1, 5, 4, 2, 6, 3],
            [1, 4, 5, 6, 2, 3],
            [2, 6, 5, 1, 4, 3],
            [2, 4, 5, 1, 6, 3],
            [2, 6, 4, 1, 5, 3],
            [6, 5, 1, 4, 2, 3]]
            
## If the nth tile in our instance comes kst, then the first element of the nth tile must be in position (6k + 1 ... 6k + 6)
first_position_constraints = [ [Implies(tile_pos[n] == (k + 1), #check for which tiles
                                        Or([board_pos[((k * num_tiles) + j)] == instance[n][1] # the first color of that tile
                                            for j in range(tile_sides)])) #iterate through the sides of the tile
                                for k in range (num_tiles)] #iterate through the tiles
                               for n in range (len(instance))] #iterate through the instance (number of tiles too)
flattened_constr = [item for sublist in first_position_constraints for item in sublist] #combine the conditions so we can add it later

#print(first_position_constraints)

# If the first color on the 3rd tile is in position 23, then the 2nd-6th colors on the 3rd tile are in positions 24,19,20,21,22.
## If the first face of the tile is in position k, then the next 5 faces are in positions (offsetted by the initial position)
# basically: it is checking where one color is and saying that if it is at a certain position,
#               it must have the follow colors of that tile in order around the tile position (the groups in the board position)
#         if the tile is not in the given location, then we check the next one
#               this mimics the rotation of a tile - rather than acutally rotating the lists of colors
#               one of these combinations should work

# need to fix this by going through the possible board positions within that tile
# maybe add something like this:     for rots in range(tile_sides)] 
#   but the question is: where do we put it so that it works?
rotation_constraints =  [ [Implies ( (And([tile_pos[tile_id] == (k + 1), 
                            board_pos[(k * num_tiles) + 0] == instance[tile_id][1]] )), #check which tile we are dealing with and where it is
                                (And([board_pos[(k * num_tiles) + j] == instance[tile_id][(j + 0) % 6] for j in range(6)]) )) 
                                        #assert that all the following tile faces match up
                            for k in range(num_tiles) ] for tile_id in range(num_tiles)]  #go through the tile numbers and tile positions

flattened_constr2 = [item for sublist in rotation_constraints for item in sublist] #combine into one list so we can add to constr


# The representation of the tiles
#               30  31
#               32  33
#               34  35
#         18  19      24  25
#         20  21      26  27
#         22  23      28  29
#   0   1       6   7       12  13
#   2   3       8   9       14  15
#   4   5       10  11      16  17

# condition for the adjacent sides of the tiles to have matching colors
match_constraints = ( And  (board_pos[1] == board_pos[22],
                            board_pos[3] == board_pos[8],
                            board_pos[6] == board_pos[23],
                            board_pos[7] == board_pos[28],
                            board_pos[9] == board_pos[14],
                            board_pos[12] == board_pos[29],
                            board_pos[19] == board_pos[34],
                            board_pos[21] == board_pos[26],
                            board_pos[24] == board_pos[35] ))

# all of the constraints involving lists
constr = board_pos_constraints + tile_constraints + no_two_same_place + no_two_face_same_color + flattened_constr + flattened_constr2 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# the actual z3 solver:

s = Solver()
s.add(constr) # add the combined list constraints
s.add(match_constraints) # this constraint needs to be added separately because
                            # it is a boolean expression not a list
if s.check() == sat: # is it satisfiable?
    m = s.model()
    r = [ m.evaluate(board_pos[i]) for i in range(num_tiles * tile_sides) ]
    print(r)
else:
    print("sadness") # this will be printed if it is not satisfiable
