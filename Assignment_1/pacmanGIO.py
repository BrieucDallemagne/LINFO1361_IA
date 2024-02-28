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

    def actions(self, state):
        # Define the possible actions for a given state
        x, y = (0, 0)
        if state.move == "Init":
            x, y =\
                next(filter(lambda t: state.grid[t[0]][t[1]] == "P",
                    [(i, j) for i in range(state.shape[0]) for j in range(state.shape[1])]))
        else:
            x, y = state.move

        actions = []

        for i in range(x+1, state.shape[0]):
            if state.grid[i][y] == "#": break
            actions.append((i, y))
        for i in range(x-1, -1, -1):
            if state.grid[i][y] == "#": break
            actions.append((i, y))
        for i in range(y+1, state.shape[1]):
            if state.grid[x][i] == "#": break
            actions.append((x, i))
        for i in range(y-1, -1, -1):
            if state.grid[x][i] == "#": break
            actions.append((x, i))
            
        return actions


    def result(self, state, action):
        # Apply the action to the state and return the new state
        if action == "Init": return state

        xPrev, yPrev = (0, 0)
        if state.move == "Init":
            xPrev, yPrev =\
                next(filter(lambda t: state.grid[t[0]][t[1]] == "P",
                    [(i, j) for i in range(state.shape[0]) for j in range(state.shape[1])]))
        else:
            xPrev, yPrev = state.move
        x, y = action

        new_grid = tuple(tuple("." if (i, j) == (xPrev, yPrev) else
                                     "P" if (i, j) == (x, y) else state.grid[i][j]
                                     for j in range(state.shape[1]))
                               for i in range(state.shape[0]))
        new_state = State(state.shape, new_grid)
        new_state.answer = state.answer - int(state.grid[x][y] == "F")
        new_state.move = action

        return new_state
        
        
    def goal_test(self, state):
    	return state.answer == 0
    
    def benchmark(self):
        width_txt = "="*64
        print("{0}\n| {1:^60} |\n{2}".format(width_txt,"Welcome to PacMan Benchmark 3000", width_txt))
        
        start = time.time_ns()
        #node, nb_explored, remaining_nodes = depth_first_tree_search(self)
        finish = time.time_ns()-start
        #print("| {0:<30} {1:>26.5f} s |".format("Depth First TREE:",finish/1e9))
        #print("| {0:<30} {1:>28} |".format("Nodes explored:",nb_explored))
        #print("| {0:<30} {1:>28} |".format("Nodes remaining:",remaining_nodes))
        #print("| {0:<30} {1:>28} |\n{2}".format("Path cost",str(node.depth) +" moves", width_txt))
        
        start = time.time_ns()
        node, nb_explored, remaining_nodes = breadth_first_tree_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |".format("Breadth First TREE:",finish/1e9))
        print("| {0:<30} {1:>28} |".format("Nodes explored:",nb_explored))
        print("| {0:<30} {1:>28} |".format("Nodes remaining:",remaining_nodes))
        print("| {0:<30} {1:>28} |\n{2}".format("Path cost",str(node.depth) +" moves", width_txt))

        start = time.time_ns()
        node, nb_explored, remaining_nodes = depth_first_graph_search(self)
        finish = time.time_ns()-start
        print("| {0:<30} {1:>26.5f} s |".format("Depth First GRAPH:",finish/1e9))
        print("| {0:<30} {1:>28} |".format("Nodes explored:",nb_explored))
        print("| {0:<30} {1:>28} |".format("Nodes remaining:",remaining_nodes))
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
        finish = time.time_ns()-start
        
        print("{0:.5f} & {1} & {2} ".format(finish/1e9, nb_explored, remaining_nodes), end="&")

        start = time.time_ns()
        node, nb_explored, remaining_nodes = breadth_first_graph_search(self)
        finish = time.time_ns()-start
        
        print("{0:.5f} & {1} & {2} ".format(finish/1e9, nb_explored, remaining_nodes), end="&")

        
        start = time.time_ns()
        #node, nb_explored, remaining_nodes = depth_first_tree_search(self)
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

    def __str__(self):
        s = str(self.move) + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s
    
    def __hash__(self) -> int:
        return hash(self.shape) + self.answer + hash(self.grid) + hash(self.move)
        # return hash(str(self))
    
    def __eq__(self, other):
        return self.shape == other.shape and self.grid == other.grid\
                and self.move == other.move and self.answer == other.answer


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

    problem.benchmark()
    exit(0)

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
