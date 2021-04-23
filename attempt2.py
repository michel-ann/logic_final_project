
from z3 import*


def rotate_list (ls, n):
    if (n >= len(ls)) :
        print("error: sadness")
    else :
        list1 = ls[n:len(ls)]
        list2 = ls[0:n]
        list1.extend(list2)
        return list1


color_arrng = [ [1, 5, 4, 2, 6, 3],
                [1, 4, 5, 6, 2, 3],
                [2, 6, 5, 1, 4, 3],
                [2, 4, 5, 1, 6, 3],
                [2, 6, 4, 1, 5, 3],
                [6, 5, 1, 4, 2, 3] ]

tiles_arr = []
for colors in color_arrng :
    for tilepos in (0, 1, 2, 3, 4, 5) :
        colorArr = []
        for i in (0, 1, 2, 3, 4, 5) :
            newList = rotate_list(colors, i)
            colorArr.append(newList) 
        for tile_option in colorArr :
            for n in tile_option :
                tiles_arr.append("x_%s = %s" % (((6 * tilepos) + n), n))



tiles_arr_all = []
startpos = 0
endpos = 6
for x in range(0, len(tiles_arr), 6) :
    tiles_arr_all.append(tiles_arr[startpos: endpos])
    endpos += 6
    startpos += 6

 #now list of lists[6]

tiles_rots = []
startpos = 0
endpos = 6
for x in range(0, len(tiles_arr_all), 6) :
    tiles_rots.append(tiles_arr_all[startpos: endpos])
    endpos += 6
    startpos += 6

by_tiles = []
startpos = 0
endpos = 6
for x in range(0, len(tiles_rots), 6) :
    by_tiles.append(tiles_rots[startpos: endpos])
    endpos += 6
    startpos += 6

# by_tiles is the list of tile possibilities. 
    # each element represents a tile
        # within that tile list, it has all of the position and rotation possibilities


# large for loop that will go through all of the options and make a bunch of lists of all the possibilities
# of combinations 

col0_opt = by_tiles[0]
col1_opt = by_tiles[1]
col2_opt = by_tiles[2]
col3_opt = by_tiles[3]
col4_opt = by_tiles[4]
col5_opt = by_tiles[5]

perms = []

for col0 in col0_opt :
    for col1 in col1_opt :
        for col2 in col2_opt :
            for col3 in col3_opt :
                for col4 in col4_opt :
                    for col5 in col5_opt :
                        listTemp = [col0, col1, col2, col3, col4, col5]
                        perms.append(listTemp)

# have all combinations of the tiles - not all legal though - need to make conditions

## need to list the condition that says only one of each position can be had
print(len(perms))


def countPresent (ls, x) :
    if x in ls[0] or x in ls[1] or x in ls[2] or x in ls[3] or x in ls[4] or x in ls[5] :
        return 1
    else :
        return 0

position_c = [ And  [Sum (countPresent(CHOSEN[0], "x_1 "), countPresent(CHOSEN[1], "x_1 "), countPresent(CHOSEN[2], "x_1 "), countPresent(CHOSEN[3], "x_1 "), countPresent(CHOSEN[4], "x_1 "), countPresent(CHOSEN[5], "x_1 ")) == 1 ]
                    [Sum (countPresent(CHOSEN[0], "x_7 "), countPresent(CHOSEN[1], "x_7 "), countPresent(CHOSEN[2], "x_7 "), countPresent(CHOSEN[3], "x_7 "), countPresent(CHOSEN[4], "x_7 "), countPresent(CHOSEN[5], "x_7 ")) == 1 ]
                    [Sum (countPresent(CHOSEN[0], "x_13 "), countPresent(CHOSEN[1], "x_13 "), countPresent(CHOSEN[2], "x_13 "), countPresent(CHOSEN[3], "x_13 "), countPresent(CHOSEN[4], "x_13 "), countPresent(CHOSEN[5], "x_13 ")) == 1 ]
                    [Sum (countPresent(CHOSEN[0], "x_19 "), countPresent(CHOSEN[1], "x_19 "), countPresent(CHOSEN[2], "x_19 "), countPresent(CHOSEN[3], "x_19 "), countPresent(CHOSEN[4], "x_19 "), countPresent(CHOSEN[5], "x_19 ")) == 1 ]
                    [Sum (countPresent(CHOSEN[0], "x_25 "), countPresent(CHOSEN[1], "x_25 "), countPresent(CHOSEN[2], "x_25 "), countPresent(CHOSEN[3], "x_25 "), countPresent(CHOSEN[4], "x_25 "), countPresent(CHOSEN[5], "x_25 ")) == 1 ]
                    [Sum (countPresent(CHOSEN[0], "x_31 "), countPresent(CHOSEN[1], "x_31 "), countPresent(CHOSEN[2], "x_31 "), countPresent(CHOSEN[3], "x_31 "), countPresent(CHOSEN[4], "x_31 "), countPresent(CHOSEN[5], "x_31 ")) == 1 ]]
def get_int (s) :
    if "1" == s :
        return 1
    elif "2" ==s :
        return 2
    elif "3" == s :
        return 3
    elif "4" == s :
        return 4
    elif "5" == s :
        return 5
    else:
        return 6

def find_element (st, ls) : #returns a string
    for tile in ls :
        for l in tile :      
            if st in l :
                return l
    
    

def get_value (st, ls) : #will return an int
    s = find_element(st, ls)
    num = s[len(s) - 1]
    return get_int(num)

#have our chosen permutation
color_c = [ And ( get_value("x1 ", CHOSEN) == get_value("x10 ", CHOSEN) )
                ( get_value("x6 ", CHOSEN) == get_value("x21 ", CHOSEN) )
                ( get_value("x7 ", CHOSEN) == get_value("x16 ", CHOSEN) )
                ( get_value("x12 ", CHOSEN) == get_value("x27 ", CHOSEN) )
                ( get_value("x11 ", CHOSEN) == get_value("x20 ", CHOSEN) )
                ( get_value("x17 ", CHOSEN) == get_value("x26 ", CHOSEN) )
                ( get_value("x19 ", CHOSEN) == get_value("x28 ", CHOSEN) )
                ( get_value("x24 ", CHOSEN) == get_value("x33 ", CHOSEN) )
                ( get_value("x29 ", CHOSEN) == get_value("x32 ", CHOSEN) ) ]


thinkominous_c = color_c + position_c

sol = Solver()

## Stopped here because we realized we couldnt really go further with this implementation
    # did too much of the iteration part so not much was left to work with for the solver

