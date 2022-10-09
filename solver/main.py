from random import shuffle
from .bfs import breadth_first_search
from .puzzle import Puzzle

def randomize_puzzle(state, prev_action):
    action = Puzzle.get_random_state(state, prev_action)
    return action

def solve_puzzle(state):
    print('Now getting the solution to the random state....')
    return breadth_first_search(state)
