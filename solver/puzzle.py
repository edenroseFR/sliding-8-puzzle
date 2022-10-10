from random import choice

class Puzzle:
    goal_state=[1,2,3,4,5,6,7,8,0]
    heuristic=None
    evaluation_function=None
    needs_hueristic=True
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
    def find_legal_actions(i,j, prev_action=''):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0 or prev_action == 'D':  # up is disable
            legal_action.remove('U')
        if i == 2 or prev_action == 'U':  # down is disable
            legal_action.remove('D')
        if j == 0 or prev_action == 'R': # left is disable
            legal_action.remove('L')
        if j == 2 or prev_action == 'L': # right is disable
            legal_action.remove('R')
        return legal_action

    @staticmethod
    def find_blank_pos(arr):
        x = arr.index(0)
        i = int(x / 3)
        j = int(x % 3)
        return i,j,x

    @staticmethod
    def get_random_move(arr, prev_action):
        i,j,_ = Puzzle.find_blank_pos(arr)
        action = choice(Puzzle.find_legal_actions(i,j, prev_action))
        return action

    def generate_child(self):
        children = []
        i,j,x = Puzzle.find_blank_pos(self.state)
        legal_actions = Puzzle.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
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
