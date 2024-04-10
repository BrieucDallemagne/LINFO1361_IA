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
        self.occupied_col = {i:{j:[] for j in range(N)} for i in range(N)} # it is a dictionary where the key is the column and there is the list of forbidden positions due to the queens in that column
    
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
        #print(available_pos, first_col)
        return available_pos

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        state = list(state)
        state[action[1]] = action[0]
        
        tmp = []
        # Need to update the forbidden positions
        # Did basic line
        tmp += [(action[0],action[1])]
        tmp += [(i%self.N,action[1]) for i in range( self.N)]
        tmp += [(action[0],i%self.N) for i in range( self.N)]
        
        # Need to do Diagonal
        for i in range(1,self.N):
            if action[0] + i < self.N and action[1] + i < self.N:
                tmp += [(action[0] + i,action[1] + i)]
            if action[0] - i >= 0 and action[1] - i >= 0:
                tmp += [(action[0] - i,action[1] - i)]
            if action[0] + i < self.N and action[1] - i >= 0:
                tmp += [(action[0] + i,action[1] - i)]
            if action[0] - i >= 0 and action[1] + i < self.N:
                tmp += [(action[0] - i,action[1] + i)]
        
        # Knight moves
        lst = [[1,4],[-1,4],[1,-4],[-1,-4],[4,1],[-4,1],[4,-1],[-4,-1],[2,3],[-2,3],[2,-3],[-2,-3],[3,2],[-3,2],[3,-2],[-3,-2]]
        for i in lst:
            if (action[0] + i[0] >= 0 and action[0] + i[0] < self.N and action[1] + i[1] >= 0 and action[1] + i[1] < self.N):
                tmp += [(action[0] + i[0],action[1] + i[1])]
        
        # Keep only unique values
        tmp = list(set(tmp))    
        
        self.occupied_col[action[1]][action[0]] = tmp
            
            
        #self.debug(state)            
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
    
    def debug(self,state):
        board = [["□"] * self.N for _ in range(self.N)]

        for i, pos in enumerate(state):
            if pos == -1:
                break
            for lst_col in self.occupied_col[i][pos]:
                board[lst_col[0]][lst_col[1]] = "■"
        
        pprint.pprint(board)
            


    def not_attacked_SPACE(self,state,queen):
        row = queen[0]
        col = queen[1]
        
        for i,pos in enumerate(state):
            if pos == -1:
                break
            if (row,col) in self.occupied_col[i][pos]:
                return False
        return True

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