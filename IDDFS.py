import Common as c
import timeit
from copy import deepcopy


params_file = "params.txt"
iddfs_file = "IDDFS_output.csv"
# [[8, 7, 6],
#  [5, 4, 3],
#  [2, 1, 0]]
template_tiles = [8, 7, 6, 5, 4, 3, 2, 1, 0]
# [[1, 2, 3],
#  [8, 0, 4],
#  [7, 6, 5]]
goal_tiles = [1, 2, 3, 8, 0, 4, 7, 6, 5]
seed, max_runs, max_level = c.read_params_file(params_file)


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
    # A dictionary of nodes holding their level in the tree and the previous node
    next_tile_string = c.convert_tiles_to_string(current_state[2])
    predecessor = {next_tile_string: [0, None]}

    # c.print_state(current_state, 0, highest_level)

    stack = [start_state]
    while stack:
        if lowest_depth > max_level:
            solution = 0
            break
        current_state = stack.pop()
        if c.check_state(current_state, goal_state):
            solution = 1
            break
        moves += 1
        path = c.get_path(current_state[2], predecessor)
        # print(f"Path {path}")
        c.print_state(current_state, moves, lowest_depth)
        for next_state in c.move(current_state):
            # print(f"Next tile {next_state[2]}")
            if next_state[2] not in path:
                new_state = deepcopy(next_state)
                nodes += 1
                current_tile_string = c.convert_tiles_to_string(current_state[2])
                stack.append(new_state)
                # print(f"{stack}")
                next_tile_string = c.convert_tiles_to_string(new_state[2])
                next_depth = predecessor[current_tile_string][0] + 1
                if next_depth > lowest_depth:
                    lowest_depth = next_depth
                predecessor[next_tile_string] = [next_depth, current_state[2]]
                # c.print_state(new_state, next_depth, highest_level)

    end_time = timeit.default_timer()
    time = end_time - start_time

    return start_state, solution, moves, nodes, time


def main():
    c.r.seed(seed)
    for run in range(max_runs):
        print(f"Run: {run}")
        goal_state = c.generate_state(goal_tiles, shuffle=False)
        # print(f"Template before {template_tiles}")
        start_state = c.generate_state(template_tiles, shuffle=True)
        # print(f"Template after {template_tiles}")
        # print(f"Start State = {start_state}")
        # start_state = [1, 2, [[5, 8, 3], [2, 6, 0], [4, 7, 1]]]
        data = solve_puzzle(start_state, goal_state)
        if run == 0:
            c.output_file(iddfs_file, data, run, "w")
        else:
            c.output_file(iddfs_file, data, run)

    return


if __name__ == '__main__':
    main()
