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
last = ""
class Pacman(Problem):
    def find_pacman(self, state):
        for i in range(0, state.shape[0]):
            for j in range(0, state.shape[1]):
                if state.grid[i][j] == 'P':
                    return (i, j)
    
    def possible_move(self, i,j, state):
        # Check if next position is valid
        return 0 <= i < state.shape[0] and 0 <= j < state.shape[1] and state.grid[i][j] != '#'

    """
    def actions2(self, state):
        # Return the list of actions that can be executed in the given state
        actions = []
        pacman = self.find_pacman(state)
                
        if self.possible_move(pacman[0]+1,pacman[1], state) :
            actions.append("UP")
        if self.possible_move(pacman[0]-1,pacman[1], state) :
            actions.append("DOWN")  
        if self.possible_move(pacman[0],pacman[1]-1, state) :
            actions.append("LEFT")
        if self.possible_move(pacman[0],pacman[1]+1, state) :
            actions.append("RIGHT")
            
        return actions
    """
        
    def actions(self, state):
        actions = []
        pacman = self.find_pacman(state)
        
        wall = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
        stillPossible = True 
        i = 1
               
        while stillPossible:
            # Explanation: We check if the next position is valid and if it is, we add it to the list of actions
            # stillPossible indicates that we can still go further. In other words didn't encounter a wall or an edge for one of the directions
            
            stillPossible = False
            
            if not wall["UP"] and self.possible_move(pacman[0] + i, pacman[1], state):
                actions.append((pacman[0] + i, pacman[1]))
                stillPossible = True
            else:
                wall["UP"] = True
                
            if not wall["DOWN"] and self.possible_move(pacman[0] - i, pacman[1], state):
                actions.append((pacman[0] - i, pacman[1]))
                stillPossible = True
            else:
                wall["DOWN"] = True
            
            if not wall["RIGHT"] and self.possible_move(pacman[0], pacman[1] + i, state):
                actions.append((pacman[0], pacman[1] + i))
                stillPossible = True
            else:
                wall["RIGHT"] = True
                
            if not wall["LEFT"] and self.possible_move(pacman[0], pacman[1] - i, state):
                actions.append((pacman[0], pacman[1] - i))
                stillPossible = True
            else:
                wall["LEFT"] = True
                
            i+=1
            
        return actions

    def result(self, state, action):
        # Return the new state reached by executing the given action in the given state
        new_grid = [list(row) for row in state.grid]
        new_fruit_count = state.answer
        pacman = self.find_pacman(state)
        
        actionTxT = f"Move to {action}"
        
        if state.grid[action[0]][action[1]] == 'F':
            new_fruit_count -= 1
            
            if self.goal_test(State(state.shape, tuple(map(tuple, new_grid)), new_fruit_count)):
                actionTxT += " Goal State"
            # Checking if there is another fruit further
                    
        new_grid[pacman[0]][pacman[1]] = "."        
        new_grid[action[0]][action[1]] = "P"
            
        # I prefer to pass the matrix visited immediately instead of handling it with the string Action
        return State(state.shape, tuple(map(tuple, new_grid)), new_fruit_count, actionTxT)
    
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
        #node, nb_explored, remaining_nodes = depth_first_tree_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |\n{2}".format("Depth First TREE:",finish/1e9, width_txt))
        
        start = time.time_ns()
        node, nb_explored, remaining_nodes = breadth_first_tree_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |".format("Breadth First TREE:",finish/1e9))
        print("| {0:<30} {1:>28} |".format("Nodes explored:",nb_explored))
        print("| {0:<30} {1:>28} |".format("Nodes remaining:",nb_explored))
        print("| {0:<30} {1:>28} |\n{2}".format("Path cost",str(node.depth) +" moves", width_txt))

        start = time.time_ns()
        node, nb_explored, remaining_nodes = depth_first_graph_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |".format("Depth First GRAPH:",finish/1e9))
        print("| {0:<30} {1:>28} |".format("Nodes explored:",nb_explored))
        print("| {0:<30} {1:>28} |".format("Nodes remaining:",nb_explored))
        print("| {0:<30} {1:>28} |\n{2}".format("Path cost",str(node.depth) +" moves", width_txt))

        start = time.time_ns()
        node, nb_explored, remaining_nodes = breadth_first_graph_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |".format("Breadth First GRAPH:",finish/1e9))
        print("| {0:<30} {1:>28} |".format("Nodes explored:",nb_explored))
        print("| {0:<30} {1:>28} |".format("Nodes remaining:",nb_explored))
        print("| {0:<30} {1:>28} |\n{2}".format("Path cost",str(node.depth) +" moves", width_txt))

    def latex(self):        
        start = time.time_ns()
        node, nb_explored, remaining_nodes = breadth_first_tree_search(self)
        #snode, nb_explored, remaining_nodes = 0, 0, 0
        finish = time.time_ns()-start
        
        print("{0:.5f} & {1} & {2} ".format(finish/1e9, nb_explored, remaining_nodes), end="&")

        start = time.time_ns()
        node, nb_explored, remaining_nodes = breadth_first_graph_search(self)
        finish = time.time_ns()-start
        
        print("{0:.5f} & {1} & {2} ".format(finish/1e9, nb_explored, remaining_nodes), end="&")

        
        start = time.time_ns()
        node, nb_explored, remaining_nodes = 0, 0, 0
        finish = time.time_ns()-start
        
        print("{0:.5f} & {1} & {2} ".format(finish/1e9, nb_explored, remaining_nodes), end="&")

        
        start = time.time_ns()
        node, nb_explored, remaining_nodes = depth_first_graph_search(self)
        finish = time.time_ns()-start
        
        print("{0:.5f} & {1} & {2} ".format(finish/1e9, nb_explored, remaining_nodes),end="\\\\")

###############
# State class #
###############
class State:
    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def find_pacman(self, state):
        for i in range(0, len(state)):
            for j in range(0, len(state[0])):
                if state[i][j] == 'P':
                    return (i, j)
        
    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s
    
    
    def __hash__(self) -> int:
        # hash for the class State
        return hash((self.find_pacman(self.grid), self.answer, self.move, self.grid))
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, State) and self.__hash__() == __value.__hash__()
    
    
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
    print(filepath.split("/")[-1], end=" & ")

    shape, initial_grid, initial_fruit_count = read_instance_file(filepath)
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init")
    problem = Pacman(init_state)
    
    problem.latex()
    print()
    exit()
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
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
    