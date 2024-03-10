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
        
    def __str__(self):
        child_str = ""
        for child in self.children.keys():
            child_str += f"\t{child} \n"
        return f"Node: {self.state} - U: {self.U} - N: {self.N} - Children: \n{child_str}"

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
            #print(f"[LOG]: Simulation {i+1}/{self.iteration} completed")
        
        ##print(root)
        
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
        
        amount_of_move = len(self.game.actions(node.state))
        
        # We found a leaf node, so We didn't expand all of his children
        if amount_of_move > len(node.children):
            #print("Leaf node")
            return node
        
        #print("Going Recursive")
        val,i = 0, 0
        for children in node.children.keys():
            if self.UCB1(children) >= val:
                val = self.UCB1(children)
                i = children
                
                
        #print(f"\tUCB1: {val} - {i}")
                
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
        actions_copy = actions.copy()
        already_expanded = node.children.values()
        
        # Remove already expanded actions
        for action in actions:
            if action in already_expanded:
                actions_copy.remove(action)
            
        actions = actions_copy
        
        action_to_perform = random.choice(actions)
        
        new_node = Node(node, self.game.result(node.state, action_to_perform))
        
        node.children[new_node] = action_to_perform
        
        """
        for action in actions:
            new_state = self.game.result(node.state, action)
            new_node = Node(node, new_state)
            node.children[new_node] = action
        """
        return new_node #random.choice(list(node.children.keys())) # Randomly select a child node

    def simulate(self, state):
        """Simulates a random play-through from the given state to a terminal state.

        Args:
            state (ShobuState): The state to simulate from.

        Returns:
            float: The utility value of the terminal state for the player to move.
        """
        # we want to know the utility for the player to move not the last player that may not be the same
        player = state.to_move
        i = 0
        while self.game.is_terminal(state) == False and i < 500:
            #print(f"\tSimulating {i+1}/500")
            action = random.choice(self.game.actions(state))
            state = self.game.result(state, action)
            i+=1
        
        #print(f"[LOG]: {self.game.utility(state, player)} - {player} - {state.to_move}")
        
        # Game utility for the player to move is either -1, 0 or 1 but we just want to know if it's a win
        if self.game.utility(state, player) > 0:
            return 1
        else:
            return 0
        
    def back_propagate(self, result, node):
        """Propagates the result of a simulation back up the tree, updating node statistics.

        Args:
            result (float): The result of the simulation.
            node (Node): The node to start backpropagation from.
        """
        # Watch out ! a win for black is a lose for white
        win = result
        player = node.state.to_move
        
        while node != None:
            node.N += 1
            if node.state.to_move == player:
                node.U += win
                val = win
            else:
                node.U += (win+1) % 2
                val = (win+1) % 2
            #print(f"For player {node.state.to_move} - Win: {val} - N: {node.N} - U: {node.U}")

            node = node.parent

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
            return float('inf')
        U = node.U # Total reward from the node so the amount of win
        N = node.parent.N # Total number of simulation from the parent node
        
        return U/n + c * math.sqrt(math.log(N)/n)