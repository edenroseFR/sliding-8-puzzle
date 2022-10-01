from random import shuffle
from .bfs import breadth_first_search
from .puzzle import Puzzle


state= [1, 2, 3, 4, 5, 6, 7, 8, 0]

def generate_random_state():
    print('Generating random state...')
    puzzle_is_solvable = False
    while not puzzle_is_solvable:
        shuffle(state)
        puzzle_is_solvable = Puzzle.is_solvable(state)
    print(state)
    print('Random state generated!')
    return state

def get_solution(state):
    print('Now getting the solution to the random state....')
    return breadth_first_search(state)
