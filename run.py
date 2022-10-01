from game import main as Sliding_Puzzle
from solver.main import generate_random_state, get_solution

random_state = generate_random_state()
puzzle_solution = get_solution(random_state)

print('starting')
print(random_state)
print(puzzle_solution)

Sliding_Puzzle.start_game(random_state, puzzle_solution)