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
        self.initial = [-1] * N
        self.positions = []
        self.board = [["□"] * N for _ in range(N)] # Create an empty board
        print(1)
                
    def compute_board(self,state,col, row):
        self.board[row][col] = "🩎"
        
        NW_length = min(row,col)
        NE_length = min(row,self.N - col - 1)
        SW_length = min(self.N - row - 1,col)
        SE_length = min(self.N - row - 1,self.N - col - 1)
        
        # compute the queen moves
        for i in range(1, self.N):
            # horizontal and vertical moves
            self.board[row][(col+i)%self.N] = "■"
            self.board[(row+i)%self.N][col] = "■"
            
            # diagonal moves
            
        for i in range(1, NW_length + 1):
            self.board[row-i][col-i] = "■"
        for i in range(1, NE_length + 1):
            self.board[row-i][(col+i)%self.N] = "■"
        for i in range(1, SW_length + 1):
            self.board[(row+i)%self.N][col-i] = "■"
        for i in range(1, SE_length + 1):
            self.board[(row+i)%self.N][(col+i)%self.N] = "■"
            
        # compute the super knight moves
        # the 4-1 moves
        for i in [-1, 1]:
            if col + i*4 >= 0:
                if row -1 >= 0:
                    self.board[row-1][col+4*i] = "■"
                if row + 1 < self.N:
                    self.board[row+1][col+4*i] = "■"
            if row + i*4 >= 0:
                if col -1 >= 0:
                    self.board[row+4*i][col-1] = "■"
                if col + 1 < self.N:
                    self.board[row+4*i][col+1] = "■"
        # the 3-2 moves
        for i in [-1, 1]:
            if col + i*3 >= 0:
                if row -2 >= 0:
                    self.board[row-2][col+3*i] = "■"
                if row + 2 < self.N:
                    self.board[row+2][col+3*i] = "■"
            if row + i*3 >= 0:
                if col -2 >= 0:
                    self.board[row+3*i][col-2] = "■"
                if col + 2 < self.N:
                    self.board[row+3*i][col+2] = "■"

        

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        # We can only fill left to right, and we can only place one queen in each column
        # get first index where self.initial[i] == -1
        col_to_fill = state.index(-1)
        
                


    def result(self, state, row):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        print(3)
        
        return state
        

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        for i in range(self.N):
            if state[i] == -1:
                return False
        for i in range(self.N):
            for j in range(i+1,self.N):
                if self.is_attacking((i,state[i]),(j,state[j])):
                            return False        
        return True

    def h(self, node):
        print(5)
        """ Return the heuristic value for a given state. Default heuristic is 0."""
        return 0
            


    def is_attacking(self,dame1,dame2):
        x1 = dame1[0]
        y1 = dame1[1]
        x2 = dame2[0]
        y2 = dame2[1]
        if x1 == x2 or y1 == y2 or abs(x1 - x2) == abs(y1 - y2) :
            return True  
        lst = [(1,4),(-1,4),(1,-4),(-1,-4),(4,1),(-4,1),(4,-1),(-4,-1),(2,3),(-2,3),(2,-3),(-2,-3),(3,2),(-3,2),(3,-2),(-3,-2)]
        for i in lst:
            if (x1 + i[0] == x2 and y1 + i[1] == y2):
                return True
            
        #same move but in diagonal
        lst2 = [(5,3),(-5,3),(5,-3),(-5,-3),(3,5),(-3,5),(3,-5),(-3,-5),(5,1),(-5,1),(5,-1),(-5,-1),(1,5),(-1,5),(1,-5),(-1,-5)]
        for i in lst2:
            if (x1 + i[0] == x2 and y1 + i[1] == y2):
                return True
        return False
        

#####################
# Launch the search #
#####################

problem = NAmazonsProblem(int(sys.argv[1]))
problem.compute_board(problem.initial,3,5)
pprint.pprint(problem.board)

start_timer = time.perf_counter()

node = astar_search(problem)

end_timer = time.perf_counter()


# example of print
path = node.path()

print('Number of moves: ', str(node.depth))

for n in path:

    print(n.state)  # assuming that the _str_ function of state outputs the correct format

    print()
    
print("Time: ", end_timer - start_timer)