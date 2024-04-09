from search import *
import numpy as np
import time
import pprint

#################
# Problem class #
#################

class NAmazonsProblem(Problem):
    """The problem of placing N amazons on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is an empress at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet. We fill in columns left to right.
    """
    def __init__(self, N):
        self.N = N
        self.initial = tuple([-1] * N)
        self.board = [["□"] * N for _ in range(N)] # Create an empty board
        self.forbidden_positions = [] # it is a set of tuple (x,y) where x is the row and y is the column
    
    def add_forbidden_positions(self, row,col):
        if (row,col) not in self.forbidden_positions:
            self.forbidden_positions.append((row,col))
    
    def compute_board(self,state,col, row):
        self.board[row][col] = "🩎"
        self.initial[col] = row
        
        NW_length = min(row,col)
        NE_length = min(row,self.N - col - 1)
        SW_length = min(self.N - row - 1,col)
        SE_length = min(self.N - row - 1,self.N - col - 1)
        
        # compute the queen moves
        for i in range(1, self.N):
            # horizontal and vertical moves
            self.add_forbidden_positions(row,(col+i)%self.N)
            self.add_forbidden_positions((row+i)%self.N,col)
            self.board[row][(col+i)%self.N] = "■"
            self.board[(row+i)%self.N][col] = "■"
            
            # diagonal moves
            
        for i in range(1, NW_length + 1):
            self.add_forbidden_positions(row-i,col-i)
            self.board[row-i][col-i] = "■"
        for i in range(1, NE_length + 1):
            self.add_forbidden_positions(row-i,(col+i)%self.N)
            self.board[row-i][(col+i)%self.N] = "■"
        for i in range(1, SW_length + 1):
            self.add_forbidden_positions((row+i)%self.N,col-i)
            self.board[(row+i)%self.N][col-i] = "■"
        for i in range(1, SE_length + 1):
            self.add_forbidden_positions((row+i)%self.N,(col+i)%self.N)
            self.board[(row+i)%self.N][(col+i)%self.N] = "■"
            
        # compute the super knight moves
        # the 4-1 moves
        for i in [-1, 1]:
            if col + i*4 >= 0:
                if row -1 >= 0:
                    self.add_forbidden_positions(row-1,col+4*i)
                    self.board[row-1][col+4*i] = "■"
                if row + 1 < self.N:
                    self.add_forbidden_positions(row+1,col+4*i)
                    self.board[row+1][col+4*i] = "■"
            if row + i*4 >= 0:
                if col -1 >= 0:
                    self.add_forbidden_positions(row+4*i,col-1)
                    self.board[row+4*i][col-1] = "■"
                if col + 1 < self.N:
                    self.add_forbidden_positions(row+4*i,col+1)
                    self.board[row+4*i][col+1] = "■"
        # the 3-2 moves
        for i in [-1, 1]:
            if col + i*3 >= 0:
                if row -2 >= 0:
                    self.add_forbidden_positions(row-2,col+3*i)
                    self.board[row-2][col+3*i] = "■"
                if row + 2 < self.N:
                    self.add_forbidden_positions(row+2,col+3*i)
                    self.board[row+2][col+3*i] = "■"
            if row + i*3 >= 0:
                if col -2 >= 0:
                    self.add_forbidden_positions(row+3*i,col-2)
                    self.board[row+3*i][col-2] = "■"
                if col + 2 < self.N:
                    self.add_forbidden_positions(row+3*i,col+2)
                    self.board[row+3*i][col+2] = "■"

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        # We can only fill left to right, and we can only place one queen in each column
        # get first index where self.initial[i] == -1
        first_col = state.index(-1)        
        available_pos = []
        
        for row in range(self.N):
            if self.not_attacked(state,(row,first_col)):
                available_pos.append((row,first_col))

        return available_pos

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        state = list(state)
        state[action[1]] = action[0]
        return tuple(state)

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        return -1 not in state

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic is 0."""
        return 0
            


    def not_attacked(self,state,dame):
        """Check if the dame is not attacked by the queens in the state

        Args:
            state (tuple): looking like (0,2,-1,-1) each index indicates a column and the value the row where the queen is placed
            dame (tuple): (row,col) where the dame is placed (0,0) is the top left corner so it is (y,x)

        Returns:
            bool: return True if the dame is not attacked by the queens in the state
        """
        x1 = dame[1]
        y1 = dame[0]
        for j in range(self.N):
            if state[j] != -1:
                x2 = j
                y2 = state[j]                
                if x1 == x2 or y1 == y2: 
                    return False
                if abs(x1 - x2) == abs(y1 - y2):
                    return False
                lst = [[1,4],[-1,4],[1,-4],[-1,-4],[4,1],[-4,1],[4,-1],[-4,-1],[2,3],[-2,3],[2,-3],[-2,-3],[3,2],[-3,2],[3,-2],[-3,-2]]
                for i in lst:
                    if (x1 + i[0] == x2 and y1 + i[1] == y2):
                        return False
            else: 
                break
        return True
        

#####################
# Launch the search #
#####################

problem = NAmazonsProblem(int(sys.argv[1]))

"""
print(problem.actions(problem.initial))
state = problem.result(problem.initial,problem.actions(problem.initial)[0])
state = problem.result(state,problem.actions(state)[0])
print(state)
print(problem.actions(state))

exit()
"""
start_timer = time.perf_counter()

node = astar_search(problem, display=True)

end_timer = time.perf_counter()

# example of print
path = node.path()

print('Number of moves: ', str(node.depth))

for n in path:

    print(n.state)  # assuming that the _str_ function of state outputs the correct format

    print()
    
print("Time: ", end_timer - start_timer)