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
    
    def __init__(self, init_state, goal=None):
        super().__init__(init_state,goal)
        self.prev_action = "" 
        self.visited = [[False for i in range(init_state.shape[1])] for j in range(init_state.shape[0])]
        self.print_visited()
        # Added a new attribute to keep track of the previous action

    def find_pacman(self, state):
        for i in range(0, state.shape[0]):
            for j in range(0, state.shape[1]):
                if state.grid[i][j] == 'P':
                    return (i, j)
    
    def possible_move(self, i,j, state):
        # Check if next position is valid
        return 0 <= i < state.shape[0] and 0 <= j < state.shape[1] and state.grid[i][j] != '#' and not self.visited[i][j]

    def actions(self, state):
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
    
    def actions2(self, state):
        actions = []
        pacman = self.find_pacman(state)
        
        stillPossible = True 
        i = 1
        
        while stillPossible:
            # Explanation: We check if the next position is valid and if it is, we add it to the list of actions
            # stillPossible indicates that we can still go further. In other words didn't encounter a wall or an edge for one of the directions
            
            stillPossible = False
            
            if self.possible_move(pacman[0] + i, pacman[1], state):
                actions.append((pacman[0] + i, pacman[1]))
                stillPossible = True
                
            if self.possible_move(pacman[0] - i, pacman[1], state):
                actions.append((pacman[0] - i, pacman[1]))
                stillPossible = True
            
            if self.possible_move(pacman[0], pacman[1] + i, state):
                actions.append((pacman[0], pacman[1] + i))
                stillPossible = True
                
            if self.possible_move(pacman[0], pacman[1] - i, state):
                actions.append((pacman[0], pacman[1] - i))
                stillPossible = True
                
            i+=1


    def result(self, state, action):
        # Return the new state reached by executing the given action in the given state
        new_grid = [list(row) for row in state.grid]
        new_fruit_count = state.answer
        pacman = self.find_pacman(state)
        
        # Test Thomas --> repeating the action
        
        
        if action == "UP":
            new_grid[pacman[0]][pacman[1]] = "."
            if state.grid[pacman[0]+1][pacman[1]] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]+1][pacman[1]] = 'P'
            self.visited[pacman[0]+1][pacman[1]] = True
        elif action == "DOWN":
            new_grid[pacman[0]][pacman[1]] = "."
            if state.grid[pacman[0]-1][pacman[1]] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]-1][pacman[1]] = 'P'
            self.visited[pacman[0]-1][pacman[1]] = True
        elif action == "LEFT":
            new_grid[pacman[0]][pacman[1]] = "."
            if state.grid[pacman[0]][pacman[1]-1] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]][pacman[1]-1] = 'P'
            self.visited[pacman[0]][pacman[1]-1] = True
        elif action == "RIGHT":
            new_grid[pacman[0]][pacman[1]] = "."
            if state.grid[pacman[0]][pacman[1]+1] == 'F':
                new_fruit_count -= 1
            new_grid[pacman[0]][pacman[1]+1] = 'P'
            self.visited[pacman[0]][pacman[1]+1] = True
            
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
        
    def print_visited(self):
        for i in range(len(self.visited)):
            for j in range(len(self.visited[0])):
                if self.visited[i][j]:
                    print("X", end="")
                else:
                    print("O", end="")
            print()




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
    
    problem.print_visited()