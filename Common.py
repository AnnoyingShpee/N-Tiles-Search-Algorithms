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
    """
    Outputs the data obtained from the algorithm and writes or appends to a CSV file
    :param file_name: The name of the file
    :param data: The data obtained from the algorithm
    :param run: The ith run of the 10 runs
    :param write_type: If "w", a new file is created or the existing file's contents are removed and the data is
                       written. If "a" the data is appended to the file
    :return:
    """
    try:
        fw = open(file_name, write_type)
        # Include headers for the CSV file
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
    """
    Convert the tiles from a 2D list representation to a string representation. Used for creating the keys for the tree
    :param tiles:
    :return:
    """
    return ''.join(str(x) for row in tiles for x in row)


def find_tile_position(tiles, number):
    """
    Finds the specified number from the tiles list
    :param tiles: 2D list
    :param number: A number from 0 to total number of tiles.
    :return:
    """
    # Get the row containing the specific number
    row = [s for s in tiles if number in s][0]
    # Equivalent to code below:
    # row = []
    # for line in shuffled_tiles:
    #     if 0 in line:
    #         row = line
    return tiles.index(row), row.index(number)


def generate_state(tiles, shuffle=False):
    """
    Generates a state as [row, col, tiles_2d] where row and col is the row number and column number of the blank tile
    and tiles_2d is a 2D list representation of the tiles puzzle. If shuffle is True, the list is shuffled before
    it is converted to a 2D list
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

    # Find the position of the blank tile
    i, j = find_tile_position(tiles_2d, 0)

    return [i, j, tiles_2d]


def check_state(state, goal_state):
    """
    Checks if the state is equal to the goal state
    :param state:
    :param goal_state:
    :return:
    """
    if state[2] == goal_state[2]:
        return True
    else:
        return False


def get_path(tiles, predecessor):
    """
    Get the path traversed by going backwards from the end tile
    :param tiles: A 2D list representation of the tiles
    :param predecessor: A dictionary representing the tree
    :return:
    """
    path = []
    while tiles:
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
    Moves the blank tile
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

