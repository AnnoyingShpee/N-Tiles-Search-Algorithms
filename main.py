import random as r

r.seed(935)
template_tiles = [[8, 7, 6],
                  [5, 4, 3],
                  [2, 1, 0]]
goal_state = [1, 1,
              [[1, 2, 3],
               [8, 0, 4],
               [7, 6, 5]]
              ]

max_runs = 10
completed_runs = 0


def shuffle_tiles():
    r.shuffle(template_tiles)
    return


def main():
    return


def check_state():
    return


if __name__ == '__main__':
    main()

