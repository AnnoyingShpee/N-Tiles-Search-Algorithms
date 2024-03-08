"""
Common functions to be used by both programs
"""
import math
import random as r
from copy import deepcopy


def read_params_file(params_file: str):
    seed = None
    max_level = None
    max_runs = None
    try:
        fr = open(params_file, "r")
        lines = fr.readlines()
        for line in lines:
            if line[0] != "#":
                line = line.replace("\n", "")
                line = line.replace(" ", "")
                tokens = line.split("=")
                if tokens[0] == "seed":
                    seed = int(tokens[1])
                elif tokens[0] == "max_runs":
                    max_runs = int(tokens[1])
                elif tokens[0] == "max_level":
                    max_level = int(tokens[1])
        fr.close()
    except Exception as e:
        print(e)
        return False, False, False
    return seed, max_runs, max_level


def output_file(file_name, data, run, write_type="a"):
    try:
        fw = open(file_name, write_type)
        if write_type == "w":
            fw.write("case_id,start_state,solution,moves,nodes,time\n")
        csv_string = f"{run}"
        # For each piece of information from the data obtained from solve_puzzle
        for item in data:
            if type(item) == list:
                csv_string += ",\"" + str(item) + "\""
            else:
                csv_string += "," + str(item)
        csv_string += "\n"
        fw.write(csv_string)
        fw.close()
    except Exception as e:
        print(e)
        return False
    return True


def convert_tiles_to_string(tiles):
    return ''.join(str(x) for row in tiles for x in row)


def generate_state(tiles, shuffle=False):
    """
    Generates the state as [row, col, tiles_2d] where row and col is the row number and column number of the blank tile
    and tiles_2d is a 2D list representation of the tiles puzzle
    :param tiles: A 1D list of the tiles
    :param shuffle: A boolean determining whether list is shuffled
    :return:
    """
    # Since the puzzle is square-shaped, the square root of the size of the 1D list is the length of the sides
    puzzle_side_len = int(math.sqrt(len(tiles)))

    tiles_2d = []

    # Shuffle the tiles
    if shuffle:
        temp = r.sample(tiles, len(tiles))
    else:
        temp = tiles

    for i in range(0, len(temp), puzzle_side_len):
        tiles_2d.append(temp[i:i+puzzle_side_len])

    # Get the row containing 0
    row = [s for s in tiles_2d if 0 in s][0]
    # Equivalent to code below:
    # row = []
    # for line in shuffled_tiles:
    #     if 0 in line:
    #         row = line
    i, j = tiles_2d.index(row), row.index(0)
    return [i, j, tiles_2d]


def check_state(state, goal_state):
    if state[2] == goal_state[2]:
        return True
    else:
        return False


def get_path(tiles, predecessor):
    path = []
    # print(f"Predecessor {predecessor}")
    while tiles:
        # print(f"Tiles {tiles}")
        # print(f"Path {path}")
        path = [tiles] + path
        tiles_string = convert_tiles_to_string(tiles)
        tiles = predecessor[tiles_string][1]
    return path


def move_blank(i, j, n):
    """
    Checks if there is a valid move and moves the blank tile of the puzzle
    :param i: The row number of the blank tile
    :param j: The column number of the blank tile
    :param n: The max row/column number of the puzzle
    :return:
    """
    if i+1 < n:
        yield i+1, j
    if i-1 >= 0:
        yield i-1, j
    if j+1 < n:
        yield i, j+1
    if j-1 >= 0:
        yield i, j-1


def move(state):
    """
    Moves the
    :param state: A list of the state of the puzzle in the form [blank_row, blank_col, [[x,x,x] , [x,x,x], [x,x,x]]]
    :return:
    """
    [i, j, grid] = deepcopy(state)
    n = len(grid)
    for pos in move_blank(i, j, n):
        i1, j1 = pos
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]
        yield [i1, j1, grid]
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]


def print_state(state, depth, lowest_depth):
    print(f"Current depth = {depth} : Lowest depth {lowest_depth} : Blank = ({state[0]}, {state[1]})")
    for row in state[2]:
        print(row)

