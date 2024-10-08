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
        self.occupied_col = {i:{j:{} for j in range(N)} for i in range(N)} # it is a dictionary where the key is the column and there is the set of forbidden positions due to the queens in that column
    
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

    def result_p(self, state, action):
        state = list(state)
        state[action[1]] = action[0]
        
        return tuple(state)


    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        state = list(state)
        state[action[1]] = action[0]
        
        tmp = {(action[0],action[1])}
        # Need to update the forbidden positions
        # Did basic line
        tmp.update({(i%self.N,action[1]) for i in range( self.N)})
        tmp.update({(action[0],i%self.N) for i in range( self.N)})
        
        # Need to do Diagonal
        for i in range(1,self.N):
            if action[0] + i < self.N and action[1] + i < self.N:
                tmp.add((action[0] + i,action[1] + i))
            if action[0] - i >= 0 and action[1] - i >= 0:
                tmp.add((action[0] - i,action[1] - i))
            if action[0] + i < self.N and action[1] - i >= 0:
                tmp.add((action[0] + i,action[1] - i))
            if action[0] - i >= 0 and action[1] + i < self.N:
                tmp.add((action[0] - i,action[1] + i))
        
        # Knight moves
        lst = [[1,4],[-1,4],[1,-4],[-1,-4],[4,1],[-4,1],[4,-1],[-4,-1],[2,3],[-2,3],[2,-3],[-2,-3],[3,2],[-3,2],[3,-2],[-3,-2]]
        for i in lst:
            if (action[0] + i[0] >= 0 and action[0] + i[0] < self.N and action[1] + i[1] >= 0 and action[1] + i[1] < self.N):
                tmp.add((action[0] + i[0],action[1] + i[1]))

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
        """ Return the heuristic value for a given state. The lower the value is the better the state is
        
        Idea of our heuristic:
            - If there is no more queens to place, we return a really small number
            - We count how many spots are yet to fill in the board and return N - left_to_fill
            - We check how many spots are not attacked and the smaller the number is the better the state is
        """
        if -1 not in node.state:
            return - self.N*self.N*100000
        
        val = 0
        
        # Check how many remaining queens can be placed
        val = (node.state.count(-1) - self.N) #adding a weight to this part
        
        val += (self.actions(node.state).__len__() - self.N)
        
        return val
        # Check how many spots are not attacked
        tmp = None
        for i in range(self.N):
            if node.state[i] != -1:
                if tmp is None:
                    tmp = self.occupied_col[i][node.state[i]]
                else:
                    tmp.update(self.occupied_col[i][node.state[i]])
        if tmp is not None:
            val += len(tmp) - self.N*self.N
        
        return val
    
    def debug(self,state):
        board = [["□"] * self.N for _ in range(self.N)]

        for i, pos in enumerate(state):
            if pos == -1:
                break
            for lst_col in self.occupied_col[i][pos]:
                board[lst_col[0]][lst_col[1]] = "■"
        
        pprint.pprint(board)
    
    
    def path_cost(self, c, state1, action, state2):
        return 0
    
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
        

def convert_state(state):
    board = [["#"] * len(state) for _ in range(len(state))]
    
    for i,pos in enumerate(state):
        if pos == -1:
            break
        board[pos][i] = "A"
        
    for i in range(len(state)):
        board[i] = "".join(board[i])
    
    return "\n".join(board)

#####################
# Launch the search #
#####################
if __name__ == "__main__":
    problem = NAmazonsProblem(int(sys.argv[1]))

    start_timer = time.perf_counter()

    node = astar_search(problem, display=False)

    end_timer = time.perf_counter()

    # example of print
    path = node.path()

    print('Number of moves: ', str(node.depth))

    for n in path:

        print(convert_state(n.state))  # assuming that the _str_ function of state outputs the correct format

        print()
        
    #print("Time: ", end_timer - start_timer)
