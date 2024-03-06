from agent import Agent
import random
import math

class Node:
    """Node Class

    A node in the MCTS tree.

    Attributes:
        parent (Node): The parent node of this node.
        state (ShobuState): The game state represented by this node.
        U (int): The total reward of the node. 
        N (int): The number of times the node has been visited.
        children (dict[Node, ShobuAction]): A dictionary mapping child nodes to their corresponding actions that lead to the state they represent.
    """
    def __init__(self, parent, state):
        """Initializes a new Node object.

        Args:
            parent (Node): The parent node of this node.
            state (ShobuState): The game state represented by this node.
        """
        self.parent = parent
        self.state = state
        self.U = 0
        self.N = 0
        self.children = {}

class UCTAgent(Agent):
    """An agent that uses the UCT algorithm to determine the best move.

    This agent extends the base Agent class, providing an implementation of the play
    method that utilizes UCT version of the MCTS algorithm.

    Attributes:
        player (int): The player id this agent represents.
        game (ShobuGame): The game the agent is playing.
        iteration (int): The number of simulations to perform in the UCT algorithm.
    """

    def __init__(self, player, game, iteration):
        """Initializes a UCTAgent with a specified player, game, and number of iterations.

        Args:
            player (int): The player id this agent represents.
            game (ShobuGame): The game the agent is playing.
            iteration (int): The number of simulations to perform in the UCT algorithm.
        """
        super().__init__(player, game)
        self.iteration = iteration

    def play(self, state, remaining_time):
        """Determines the next action to take in the given state.

        Args:
            state (ShobuState): The current state of the game.
            remaining_time (float): The remaining time in seconds that the agent has to make a decision.

        Returns:
            ShobuAction: The chosen action.
        """
        return self.uct(state)

    def uct(self, state):
        """Executes the UCT algorithm to find the best action from the current state.

        Args:
            state (ShobuState): The current state of the game.

        Returns:
            ShobuAction: The action leading to the best-perceived outcome based on UCT algorithm.
        """
        root = Node(None, state)
        for i in range(self.iteration):
            leaf = self.select(root)
            child = self.expand(leaf)
            result = self.simulate(child.state)
            self.back_propagate(result, child)
            print(f"[LOG]: Simulation {i+1}/{self.iteration} completed")
        max_state = max(root.children, key=lambda n: n.N)
        return root.children.get(max_state)

    def select(self, node):
        """Selects a leaf node using the UCB1 formula to maximize exploration and exploitation.

        A node is considered a leaf if it has a potential child from which no simulation has yet been initiated or when the game is finished.

        Args:
            node (Node): The node to select from.

        Returns:
            Node: The selected leaf node.
        """
        
        # We found a leaf node
        if len(node.children) == 0:
            return node
        
        val,i = 0, 0
        for children in node.children.keys():
            if self.UCB1(children) >= val:
                val = self.UCB1(children)
                i = children
                
        return self.select(i) # Recursive approach until we hit a leaf node
    
    def expand(self, node):
        """Expands a node by adding a child node to the tree for an unexplored action.

        This function generates all possible actions from the current state represented by the node if they haven't been explored yet. 
        For each unexplored action, a new child node is created, representing the state resulting from that action. The function then 
        selects one of these new child nodes and returns it. If the node represents a terminal state it effectively returns the node itself, 
        indicating that the node cannot be expanded further.

        Args:
            node (Node): The node to expand. This node represents the current state from which we want to explore possible actions.

        Returns:
            Node: The newly created child node representing the state after an unexplored action. If the node is at a terminal state, the node itself is returned.
        """
        # Check if the node is a terminal state
        if self.game.is_terminal(node.state):
            return node
        
        # Creating all legal actions from this state
        actions = self.game.actions(node.state)
        
        for action in actions:
            new_state = self.game.result(node.state, action)
            new_node = Node(node, new_state)
            node.children[new_node] = action
        
        return random.choice(list(node.children.keys())) # Randomly select a child node

    def simulate(self, state):
        """Simulates a random play-through from the given state to a terminal state.

        Args:
            state (ShobuState): The state to simulate from.

        Returns:
            float: The utility value of the terminal state for the player to move.
        """
        while self.game.is_terminal(state) == False:
            action = random.choice(self.game.actions(state))
            state = self.game.result(state, action)
            
            # Perhaps should add an escape sequence (for example stop after 50 moves)
        return self.game.utility(state, self.player)

    def back_propagate(self, result, node):
        """Propagates the result of a simulation back up the tree, updating node statistics.

        Args:
            result (float): The result of the simulation.
            node (Node): The node to start backpropagation from.
        """
        # Watch out ! a win for black is a lose for white
        win = result 
        while node != None:
            node.N += 1 
            node.U += win
            node = node.parent
            win = (win + 1) % 2 # Switch between 0 and 1

    def UCB1(self, node):
        """Calculates the UCB1 value for a given node.

        Args:
            node (Node): The node to calculate the UCB1 value for.

        Returns:
            float: The UCB1 value.
        """
        # Find if this will result into a win or lose for the given player        
        c = math.sqrt(2)
        n = node.N
        if n == 0:
            n = 1
        U = node.U # Total reward from the node so the amount of win
        N = node.parent.N # Total number of simulation from the parent node
        if N == 0:
            N = 1
        
        return U/n + c * math.sqrt(math.log(N)/n)
    