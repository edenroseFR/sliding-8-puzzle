from random import choice

class Puzzle:
    goal_state=[1,2,3,4,5,6,7,8,0]
    heuristic=None
    evaluation_function=None
    needs_hueristic=False
    num_of_instances=0
    def __init__(self,state,parent,action,path_cost,needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.generate_heuristic()
            self.evaluation_function=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1

    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])

    def generate_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:  # up is disable
            legal_action.remove('U')
        elif i == 2:  # down is disable
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')
        return legal_action

    @staticmethod
    def find_blank_pos(arr):
        x = arr.index(0)
        i = int(x / 3)
        j = int(x % 3)
        return i,j,x

    @staticmethod
    def get_random_state(arr, n):
        actions = []
        for _ in range(n):
            i,j,_ = Puzzle.find_blank_pos(arr)
            action = choice(Puzzle.find_legal_actions(i,j))
            actions.append(action)
            grid = [
                arr[:3],
                arr[3:6],
                arr[6:9],
            ]
            if action == 'L':
                row = i
                col = j-1
            elif action == 'R':
                row = i
                col = j+1
            elif action == 'U':
                row = i-1
                col = j
            else:
                row = i+1
                col = j
            grid[i][j] = grid[row][col]
            grid[row][col] = 0
            arr = []
            for x in grid:
                for y in x:
                    arr.append(y)
        actions.reverse()
        return actions, arr


    def generate_child(self):
        children=[]
        i,j,x = Puzzle.find_blank_pos(self.state)
        legal_actions=Puzzle.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action is 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action is 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action is 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action is 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,1,self.needs_hueristic))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution


    # This function returns true
    # if given 8 puzzle is solvable.
    # Read more: https://datawookie.dev/blog/2019/04/sliding-puzzle-solvable/
    @staticmethod
    def is_solvable(tiles):
        """
        Check whether a 3x3 sliding puzzle is solvable.

        Checks the number of "inversions". If this is odd then the puzzle configuration is not solvable.

        An inversion is when two tiles are in the wrong order.

        For example, the sequence 1, 3, 4, 7, 0, 2, 5, 8, 6 has six inversions:

        3 > 2
        4 > 2
        7 > 2
        7 > 5
        7 > 6
        8 > 6

        The empty tile is ignored.
        """
        count = 0

        for i in range(8):
            for j in range(i+1, 9):
                if tiles[j] and tiles[i] and tiles[i] > tiles[j]:
                    count += 1

        return count % 2 == 0


