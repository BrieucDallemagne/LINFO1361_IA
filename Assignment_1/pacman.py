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
        # Return the list of actions that can be executed in the given state
        actions = []
        for i in range(0, state.shape[0]):
            for j in range(0, state.shape[1]):
                if state.grid[i][j] == 'P':
                    if i > 0 and state.grid[i-1][j] != 'W':
                        actions.append("UP")
                    if i < state.shape[0] - 1 and state.grid[i+1][j] != 'W':
                        actions.append("DOWN")
                    if j > 0 and state.grid[i][j-1] != 'W':
                        actions.append("LEFT")
                    if j < state.shape[1] - 1 and state.grid[i][j+1] != 'W':
                        actions.append("RIGHT")
        return actions


    def result(self, state, action):
        # Return the new state reached by executing the given action in the given state
        new_grid = [list(row) for row in state.grid]
        new_fruit_count = state.answer
        for i in range(0, state.shape[0]):
            for j in range(0, state.shape[1]):
                if state.grid[i][j] == 'P':
                    if action == "UP":
                        if state.grid[i-1][j] == 'F':
                            new_fruit_count -= 1
                        new_grid[i][j] = ' '
                        new_grid[i-1][j] = 'P'
                    if action == "DOWN":
                        if state.grid[i+1][j] == 'F':
                            new_fruit_count -= 1
                        new_grid[i][j] = ' '
                        new_grid[i+1][j] = 'P'
                    if action == "LEFT":
                        if state.grid[i][j-1] == 'F':
                            new_fruit_count -= 1
                        new_grid[i][j] = ' '
                        new_grid[i][j-1] = 'P'
                    if action == "RIGHT":
                        if state.grid[i][j+1] == 'F':
                            new_fruit_count -= 1
                        new_grid[i][j] = ' '
                        new_grid[i][j+1] = 'P'
        return State(state.shape, tuple(map(tuple, new_grid)), new_fruit_count, action)
        
    def goal_test(self, state):
        # Return True if the state is a goal state
        return state.answer == 0



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
