from z3 import *

num_tiles = 6
tile_sides = 6
colors = 6

## the positions of the tiles -> the index represents which tile
tile_pos =  [ Int("position of tile number %s" % (i+1)) for i in range(num_tiles) ]
## the colors of the positions on the board -> the index represents the board position
board_pos = [ Int("Board position_%s" % i) for i in range(num_tiles * tile_sides)]

## Every position has 1 of 6 colors
board_pos_constraints = [And(1 <= board_pos[i], board_pos[i] <= colors) for i in range(num_tiles * tile_sides)]

## Every tile is in position 1 .. 6
tile_constraints = [And(1 <= tile_pos[i], tile_pos[i] <= num_tiles) for i in range(num_tiles)]

## No two tiles are in the same place
no_two_same_place = [ Distinct(tile_constraints) ]

## No tile has the same color twice 
no_two_face_same_color = [ Distinct(board_pos[((i * tile_sides)+1):((i * tile_sides) + tile_sides)])
                           for i in range(num_tiles)]
            
instance = [[1, 5, 4, 2, 6, 3], # this is the first tile in our input, but we don't know where it goes on the board
            [1, 4, 5, 6, 2, 3],
            [2, 6, 5, 1, 4, 3],
            [2, 4, 5, 1, 6, 3],
            [2, 6, 4, 1, 5, 3],
            [6, 5, 1, 4, 2, 3]]
            
## If the nth tile in our instance comes kst, then the first element of the nth tile tile must be in position (6k + 1 ... 6k + 6)
first_position_constraints = [ [Implies(tile_pos[n] == k,
                                        Or([board_pos[((k * num_tiles) + j)] == instance[n][1] ## the first color of that tile
                                            for j in range(tile_sides)]))
                                for k in range (num_tiles)] 
                               for n in range (len(instance))]
flattened_constr = [item for sublist in first_position_constraints for item in sublist]

# If the first color on the 3rd tile is in position 23, then the 2nd-6th colors on the 3rd tile are in positions 24,19,20,21,22.
## If the first face of the tile is in position k, then the next 5 faces are in positions k + ((k + 1) mod 6) to k + (k + 6 mod 6) // something like that
rotation_constraints = [ [Implies ( (And(tile_pos[tile_id] == (k + 1), board_pos[(k * num_tiles)] == instance[tile_id][1])), #check which tile we are dealing with and where it is
                                        (And([board_pos[(k * num_tiles) + j] == instance[tile_id][j] for j in range(6)]))) #assert that all the following tile faces match up
                                        for k in range(6) ] for tile_id in range(6)] #go through the tile numbers and tile positions

flattened_constr2 = [item for sublist in rotation_constraints for item in sublist]

## The following faces have to be the same 
match_constraints = ( And (board_pos[1] == board_pos[22],  #for the colors
                            board_pos[3] == board_pos[8],
                            board_pos[6] == board_pos[23],
                            board_pos[7] == board_pos[28],
                            board_pos[9] == board_pos[14],
                            board_pos[12] == board_pos[29],
                            board_pos[19] == board_pos[34],
                            board_pos[21] == board_pos[26],
                            board_pos[24] == board_pos[35] ))

constr = board_pos_constraints + tile_constraints + no_two_same_place + no_two_face_same_color + flattened_constr + flattened_constr2 

s = Solver()
s.add(constr)
s.add(match_constraints)
if s.check() == sat:
    m = s.model()
    r = [ m.evaluate(board_pos[i]) for i in range(num_tiles * tile_sides) ]
    print(r)
else:
    print("sadness")
