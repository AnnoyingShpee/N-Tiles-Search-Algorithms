import timeit
import math
import random as r
from copy import deepcopy


iddfs_file = "IDDFS_output.csv"
# [[8, 7, 6],
#  [5, 4, 3],
#  [2, 1, 0]]
template_tiles_list = [8, 7, 6, 5, 4, 3, 2, 1, 0]
# [[1, 2, 3],
#  [8, 0, 4],
#  [7, 6, 5]]
goal_tiles_list = [1, 2, 3, 8, 0, 4, 7, 6, 5]
seed, max_runs, max_level = 935, 10, 30


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


def solve_puzzle(start_state, goal_state):
    """
    This function attempts to find a solution to the N-tile puzzle using a non-recursive Depth-First Search algorithm
    with Iterative Deepening.
    :param start_state: A list containing the row and column number of the blank tile, and a 2D list of the start tiles.
    :param goal_state: A list containing the row and column number of the blank tile, and a 2D list of the goal tiles.
    :return:
    """
    # Start the timer
    start_time = timeit.default_timer()
    # 1 or 0 on whether a solution is found or not
    solution = 0
    # The depth level from the start state to the goal state
    moves = 0
    # Total number of nodes opened
    nodes = 0
    # Lowest depth allowed for the DFS Tree to go down to.
    lowest_depth = 1
    # Initialise the current state with the start state
    current_state = start_state
    # Convert the 2D current state tiles into a 1D string representation. The string representations will be used as the
    # key for the dictionary.
    tiles_string = convert_tiles_to_string(current_state[2])
    # A dictionary representing a tree where the nodes/states contain information in key-value pairs where:
    # Key = The 1D string representation of the 2D tiles of the state
    # Value = A list containing 2 items: [0]depth level in the tree , [1]tiles of the state before it
    tree = {tiles_string: [0, None]}

    # The lowest_depth increases after every iteration. Loop will stop when lowest depth exceeds max_level
    while lowest_depth <= max_level:
        # Initialise the stack with the start state
        stack = [start_state]
        # While the stack is not empty
        while stack:
            # Remove the top element of the stack and use it as the current state
            current_state = stack.pop()
            # Check if the current state is equal to the goal state
            if check_state(current_state, goal_state):
                solution = 1
                current_tile_string = convert_tiles_to_string(current_state[2])
                moves = tree[current_tile_string][0]
                break
            # Get the path traversed by the algorithm
            path = get_path(current_state[2], tree)
            # Get the next valid states
            for next_state in move(current_state):
                nodes += 1
                # If the state is not part of the path:
                if next_state[2] not in path:
                    # Since lists are passed by reference, a new object for it needs to be created
                    new_state = deepcopy(next_state)
                    current_tile_string = convert_tiles_to_string(current_state[2])
                    # The depth of the next valid state is the depth level of the current state + 1
                    next_depth = tree[current_tile_string][0] + 1
                    # If the next depth does not exceed the lowest allowed depth of the tree, add the state to the top
                    # of the stack to be traversed.
                    if next_depth <= lowest_depth:
                        stack.append(new_state)
                    # Regardless of whether the state's depth exceeds the lowest allowed depth, add it to the tree for
                    # faster lookup in future iterations
                    tiles_string = convert_tiles_to_string(new_state[2])
                    tree[tiles_string] = [next_depth, current_state[2]]
        # Increase the allowed depth level to be searched
        lowest_depth += 1
        if solution:
            break

    # Get the total time taken by the algorithm
    end_time = timeit.default_timer()
    time = end_time - start_time

    # If no solution is found, set the move as 0
    if not solution:
        moves = 0

    return start_state, solution, moves, nodes, time


def main():
    r.seed(seed)
    # For each run case
    for run in range(max_runs):
        print(f"Run: {run}")
        # Shuffle the goal and template lists and create the goal and start states.
        # The states are represented as [x, y, list] where x and y are the row and column number of the blank tile
        # respectively and list is a 2D list representation of the tiles
        goal_state = generate_state(goal_tiles_list, shuffle=False)
        start_state = generate_state(template_tiles_list, shuffle=True)
        # Run the algorithm
        data = solve_puzzle(start_state, goal_state)
        # For the first run, create a new file or erase the existing file's contents and write the data
        if run == 0:
            output_file(iddfs_file, data, run, "w")
        else:
            output_file(iddfs_file, data, run)

    return


if __name__ == '__main__':
    main()
