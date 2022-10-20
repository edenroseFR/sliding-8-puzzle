from .astar import astar_search
from .bfs import breadth_first_search
from .puzzle import Puzzle

def randomize_move(state, prev_action):
    action = Puzzle.get_random_move(state, prev_action)
    return action

def solve_puzzle(state, algo):
    print('Now getting the solution to the random state....')
    if algo == 'bfs':
        return breadth_first_search(state)
    elif algo == 'astar':
        return astar_search(state)