from random import shuffle
from .bfs import breadth_first_search
from .puzzle import Puzzle



# def generate_random_state():
#     print('Generating random state...')
#     puzzle_is_solvable = False
#     while not puzzle_is_solvable:
#         shuffle(state)
#         puzzle_is_solvable = Puzzle.is_solvable(state)
#     print(state)
#     print('Random state generated!')
#     return state

def randomize_puzzle(state, prev_action):
    action = Puzzle.get_random_state(state, prev_action)
    return action

def solve_puzzle(state):
    print('Now getting the solution to the random state....')
    return breadth_first_search(state)
