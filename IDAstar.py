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
    # Total number of moves made
    moves = 0
    # Total number of nodes opened
    nodes = 0
    # Lowest depth of the DFS Tree
    lowest_depth = 0
    # Initialise the current state with the start state
    current_state = start_state
    # The threshold that determines the maximum f-score allowed to open a node
    threshold = manhattan_distance(current_state[2], goal_state[2])

    current_tile_string = c.convert_tiles_to_string(current_state[2])
    # A dictionary of nodes holding a list of values corresponding to
    # [0]their depth in the tree, [1]the states  and [2]the f-score of the state/tiles
    tree = {current_tile_string: [0, None, manhattan_distance(current_state[2], goal_state[2])]}
    # A set containing the f-scores higher than threshold
    visited_f_scores = {threshold}

    while lowest_depth <= max_level:
        stack = [start_state]
        # Get the smallest value of the f-scores that were previously larger than the threshold and set it as the new
        # threshold
        threshold = min(visited_f_scores)
        # Remove the threshold
        visited_f_scores.remove(threshold)
        while stack:
            current_state = stack.pop()
            current_tile_string = c.convert_tiles_to_string(current_state[2])
            if c.check_state(current_state, goal_state):
                solution = 1
                moves = tree[current_tile_string][0]
                break
            path = c.get_path(current_state[2], tree)
            for next_state in c.move(current_state):
                nodes += 1
                if next_state[2] not in path:
                    new_state = deepcopy(next_state)
                    next_depth = tree[current_tile_string][0] + 1
                    if next_depth > lowest_depth:
                        lowest_depth = next_depth
                    f_score = next_depth + manhattan_distance(next_state[2], goal_state[2])
                    if f_score <= threshold:
                        stack.append(new_state)
                    else:
                        visited_f_scores.add(f_score)
                    next_tile_string = c.convert_tiles_to_string(new_state[2])
                    # c.print_state(current_state, next_depth, lowest_depth)
                    tree[next_tile_string] = [next_depth, current_state[2], f_score]
                    # c.print_state(new_state, next_depth, highest_level)

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
