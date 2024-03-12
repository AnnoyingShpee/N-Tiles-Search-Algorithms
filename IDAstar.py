import Common as c
import timeit
from copy import deepcopy

params_file = "params.txt"
ida_file = "IDAstar_output.csv"
# [[8, 7, 6],
#  [5, 4, 3],
#  [2, 1, 0]]
template_tiles_list = [8, 7, 6, 5, 4, 3, 2, 1, 0]
# [[1, 2, 3],
#  [8, 0, 4],
#  [7, 6, 5]]
goal_tiles_list = [1, 2, 3, 8, 0, 4, 7, 6, 5]
seed, max_runs, max_level = c.read_params_file(params_file)


def manhattan_distance(tiles, goal_tiles):
    """
    Calculates the "distance" of the current tiles from the goal tiles
    :param tiles:
    :param goal_tiles:
    :return:
    """
    h = 0
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            tile = tiles[i][j]
            if tile != 0:
                row, col = c.find_tile_position(goal_tiles, tile)
                h += abs(row - i) + abs(col - j)
    return h


def solve_puzzle(start_state, goal_state):
    """
    This function attempts to find the smallest number of moves to solve the N-tile puzzle using Iterative Deepening
    Depth-First Search algorithm.
    :param start_state: A list containing the row and column number of the blank tile, and the start tiles
    :param goal_state: A list containing the row and column number of the blank tile, and the goal tiles
    :return:
    """
    # Get the start time
    start_time = timeit.default_timer()
    # 1 or 0 on whether a solution is found or not
    solution = 0
    # The depth level from the start state to the goal state
    moves = 0
    # Total number of nodes opened
    nodes = 0
    # Lowest depth of the DFS Tree
    lowest_depth = 0
    # Initialise the current state with the start state
    current_state = start_state
    # The threshold that determines the maximum f-score that a state is allowed in order to open it
    threshold = manhattan_distance(current_state[2], goal_state[2])

    tile_string = c.convert_tiles_to_string(current_state[2])
    # A dictionary representing a tree where the nodes/states contain information in key-value pairs where:
    # Key = The 1D string representation of the 2D tiles of the state
    # Value = A list containing 3 items: [0]depth level in the tree , [1]tiles of the state before it,
    #                                    [2]state's f-score
    tree = {tile_string: [0, None, manhattan_distance(current_state[2], goal_state[2])]}
    # A set containing the f-scores higher than threshold
    visited_f_scores = {threshold}

    # The lowest_depth increases when a state's depth exceeds it and the depth is replaced.
    # Loop will stop when lowest depth exceeds max_level.
    while lowest_depth <= max_level:
        stack = [start_state]
        # Get the smallest value from the set of f-scores that were previously larger than the threshold and set it as
        # the new threshold
        threshold = min(visited_f_scores)
        # Remove the threshold from the set
        visited_f_scores.remove(threshold)
        while stack:
            # Remove the top element from the stack and set it as the current state
            current_state = stack.pop()
            # Check if state is equal to the goal state
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
                # If the state is not in the path:
                if next_state[2] not in path:
                    # Since lists are passed by reference, a new object for it needs to be created
                    new_state = deepcopy(next_state)
                    current_tile_string = c.convert_tiles_to_string(current_state[2])
                    # The depth of the next valid state is the depth level of the current state + 1
                    next_depth = tree[current_tile_string][0] + 1
                    # If the depth of the valid state is greater than the lowest depth, replace it
                    if next_depth > lowest_depth:
                        lowest_depth = next_depth
                    # Calculate the f_score of the next state
                    f_score = next_depth + manhattan_distance(next_state[2], goal_state[2])
                    # If the f_score is less than the threshold, add it to the stack to be opened
                    if f_score <= threshold:
                        stack.append(new_state)
                    # Else, add it to the set of visited f-scores
                    else:
                        visited_f_scores.add(f_score)
                    next_tile_string = c.convert_tiles_to_string(new_state[2])
                    tree[next_tile_string] = [next_depth, current_state[2], f_score]

        if solution:
            break

    end_time = timeit.default_timer()
    time = end_time - start_time

    return start_state, solution, moves, nodes, time


def main():
    c.r.seed(seed)
    # goal_state = c.generate_state(goal_tiles_list, shuffle=False)
    # # print(f"Template before {template_tiles}")
    # start_state = c.generate_state(template_tiles_list, shuffle=True)
    # data = solve_puzzle(start_state, goal_state)
    # print(data)
    for run in range(max_runs):
        print(f"Run: {run}")
        goal_state = c.generate_state(goal_tiles_list, shuffle=False)
        # print(f"Template before {template_tiles}")
        start_state = c.generate_state(template_tiles_list, shuffle=True)
        # print(f"Template after {template_tiles}")
        # print(f"Start State = {start_state}")
        # start_state = [1, 2, [[5, 8, 3], [2, 6, 0], [4, 7, 1]]]
        data = solve_puzzle(start_state, goal_state)
        if run == 0:
            c.output_file(ida_file, data, run, "w")
        else:
            c.output_file(ida_file, data, run)

    return


if __name__ == '__main__':
    main()
