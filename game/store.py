show_clicked = False
solve_clicked = False
puzzle_solved = True
start_shuffle = False
shuffle_times = 0
solving = False
active_algo = 'bfs'
algorithms = {
    'bfs': 'selected',
    'astar': 'not-selected'
}

def update_algorithms(activated_algo):
    for algo, state in algorithms.items():
        if algo == activated_algo and state != 'selected':
            algorithms[algo] = 'selected'
        elif state != 'not-selected':
            algorithms[algo] = 'not-selected'