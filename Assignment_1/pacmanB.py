"""
Name of the author(s):
- Charles Lohest <charles.lohest@uclouvain.be>
"""
import time
import sys
from search import *


#################
# Problem class #
#################
dico = {}
class Pacman(Problem):

    def find_pacman(self, state):
        for i in range(0, state.shape[0]):
            for j in range(0, state.shape[1]):
                if state.grid[i][j] == 'P':
                    return (i, j)
    
    def possible_move(self, i,j, state):
        # Check if next position is valid
        # return True if valid, False otherwise
        return 0 <= i < state.shape[0] and 0 <= j < state.shape[1] and state.grid[i][j] != '#' and state.grid[i][j] != ' '
    
    def keep_track(self, i,j, state, last_action):
        # recieve last action and keep trying this action until it is not possible
        # return the number of time the action was possible
        count = 1
        while self.possible_move(i,j, state):
            count += 1
            if last_action == "UP":
                i += 1
            elif last_action == "DOWN":
                i -= 1
            elif last_action == "LEFT":
                j -= 1
            elif last_action == "RIGHT":
                j += 1
        return count


    def actions(self, state):
        # Return the list of actions that can be executed in the given state, n time the same action is also considered as 1 action
        actions = []
        chosed = " "
        pacman = self.find_pacman(state)
        if self.possible_move(pacman[0]+1, pacman[1], state):
            actions.append("UP")
            chosed = "UP"
            count = self.keep_track(pacman[0]+1, pacman[1], state, chosed)
            if count > 1:
                for i in range(2, count):
                    actions.append("UP"*i)
        if self.possible_move(pacman[0]-1, pacman[1], state):
            actions.append("DOWN")
            chosed = "DOWN"
            count = self.keep_track(pacman[0]-1, pacman[1], state, chosed)
            if count > 1:
                for i in range(2, count):
                    actions.append("DOWN"*i)
        if self.possible_move(pacman[0], pacman[1]-1, state):
            actions.append("LEFT")  
            chosed = "LEFT"
            count = self.keep_track(pacman[0], pacman[1]-1, state, chosed)
            if count > 1:
                for i in range(2, count):
                    actions.append("LEFT"*i)
        if self.possible_move(pacman[0], pacman[1]+1, state ):
            actions.append("RIGHT")
            chosed = "RIGHT"
            count = self.keep_track(pacman[0], pacman[1]+1, state, chosed)
            if count > 1:
                for i in range(2, count):
                    actions.append("RIGHT"*i)

        for act in actions:
            print(act)
            
        
        return actions
    
    def count_nbr_time_same_action(self, action):
        act = action[0]
        count = 1
        while action[count] == act:
            count += 1
        return count



    def result(self, state, action):
        # Return the new state reached by executing the given action in the given state
        new_grid = [list(row) for row in state.grid]
        new_fruit_count = state.answer
        pacman = self.find_pacman(state)
        if action == "UP":
            new_grid[pacman[0]][pacman[1]] = ' '
            if state.grid[pacman[0]+1][pacman[1]] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]+1][pacman[1]] = 'P'
        elif action == "DOWN":
            new_grid[pacman[0]][pacman[1]] = ' '
            if state.grid[pacman[0]-1][pacman[1]] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]-1][pacman[1]] = 'P'
        elif action == "LEFT":
            new_grid[pacman[0]][pacman[1]] = ' '
            if state.grid[pacman[0]][pacman[1]-1] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]][pacman[1]-1] = 'P'
        elif action == "RIGHT":
            new_grid[pacman[0]][pacman[1]] = ' '
            if state.grid[pacman[0]][pacman[1]+1] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]][pacman[1]+1] = 'P'
        return State(state.shape, tuple(map(tuple, new_grid)), new_fruit_count, action)
    
    def goal_test(self, state):
        # Return True if the state is a goal state
        return state.answer == 0
    
        
    def benchmark(self):
        """Benchmark for question 3

        Returns:
            None: none
        """
        width_txt = "="*64
        print("{0}\n| {1:^60} |\n{2}".format(width_txt,"Welcome to PacMan Benchmark 3000", width_txt))
        
        start = time.time_ns()
        depth_first_tree_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |\n{2}".format("Depth First TREE:",finish/1e9, width_txt))
        
        start = time.time_ns()
        breadth_first_tree_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |\n{2}".format("Breadth First TREE:",finish/1e9, width_txt))

        start = time.time_ns()
        depth_first_graph_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |\n{2}".format("Depth First GRAPH:",finish/1e9, width_txt))

        start = time.time_ns()
        breadth_first_graph_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |\n{2}".format("Breadth First GRAPH:",finish/1e9, width_txt))
        





###############
# State class #
###############
class State:
    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move
        
    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s
    
    
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()
    shape_x, shape_y = tuple(map(int, lines[0].split()))
    initial_grid = [tuple(row) for row in lines[1:1 + shape_x]]
    initial_fruit_count = sum(row.count('F') for row in initial_grid)
    return (shape_x, shape_y), initial_grid, initial_fruit_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./Pacman.py <path_to_instance_file>")
    filepath = sys.argv[1]
    shape, initial_grid, initial_fruit_count = read_instance_file(filepath)
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init")
    problem = Pacman(init_state)
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    end_timer = time.perf_counter()
    # Example of print
    path = node.path()
    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)
    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)