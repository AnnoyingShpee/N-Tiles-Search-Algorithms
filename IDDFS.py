import Common as c
import timeit
from copy import deepcopy


params_file = "params.txt"
iddfs_file = "IDDFS_output.csv"
# [[8, 7, 6],
#  [5, 4, 3],
#  [2, 1, 0]]
template_tiles_list = [8, 7, 6, 5, 4, 3, 2, 1, 0]
# [[1, 2, 3],
#  [8, 0, 4],
#  [7, 6, 5]]
goal_tiles_list = [1, 2, 3, 8, 0, 4, 7, 6, 5]
seed, max_runs, max_level = c.read_params_file(params_file)


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
    tiles_string = c.convert_tiles_to_string(current_state[2])
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
            if c.check_state(current_state, goal_state):
                solution = 1
                current_tile_string = c.convert_tiles_to_string(current_state[2])
                moves = tree[current_tile_string][0]
                break
            # Get the path traversed by the algorithm
            path = c.get_path(current_state[2], tree)
            # Get the next valid states
            for next_state in c.move(current_state):
                nodes += 1
                # If the state is not part of the path:
                if next_state[2] not in path:
                    # Since lists are passed by reference, a new object for it needs to be created
                    new_state = deepcopy(next_state)
                    current_tile_string = c.convert_tiles_to_string(current_state[2])
                    # The depth of the next valid state is the depth level of the current state + 1
                    next_depth = tree[current_tile_string][0] + 1
                    # If the next depth does not exceed the lowest allowed depth of the tree, add the state to the top
                    # of the stack to be traversed.
                    if next_depth <= lowest_depth:
                        stack.append(new_state)
                    # Regardless of whether the state's depth exceeds the lowest allowed depth, add it to the tree for
                    # faster lookup in future iterations
                    tiles_string = c.convert_tiles_to_string(new_state[2])
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
    c.r.seed(seed)
    # For each run case
    for run in range(max_runs):
        print(f"Run: {run}")
        # Shuffle the goal and template lists and create the goal and start states.
        # The states are represented as [x, y, list] where x and y are the row and column number of the blank tile
        # respectively and list is a 2D list representation of the tiles
        goal_state = c.generate_state(goal_tiles_list, shuffle=False)
        start_state = c.generate_state(template_tiles_list, shuffle=True)
        # Run the algorithm
        data = solve_puzzle(start_state, goal_state)
        # For the first run, create a new file or erase the existing file's contents and write the data
        if run == 0:
            c.output_file(iddfs_file, data, run, "w")
        else:
            c.output_file(iddfs_file, data, run)

    return


if __name__ == '__main__':
    main()
