# Implémentation simple d'alpha-beta pruning

class Node:
    def __init__(self, color,*args,) -> None:
        if len(args) == 0:
            self.val = None
        else:
            self.val = args[0]
        self.color = color
        
        self.children = []
        self.visited = False # useful for alpha-beta analysis

        
    def add_child(self, *child):
        for c in child:
            self.children.append(child)
    
    def get_children(self):
        return self.children
    
    def __str__(self) -> str:
        if len(self.children) == 0:
            return f"Leaf({self.val}) {self.visited:>20}"
        else:
            cString = ""
            for c in self.children:
                cString += f"{c}\n"
            return f"Node({self.val}) {self.visited:>20} \n {cString}"
        
def minmaxAB(state, depth, alpha, beta, player):
    # we will say that white is the maximizing player and black the minimizing player
    
    if depth == 0 or state.is_terminal():
        return state.eval(), None
    
    if player == "white":
        value = -float("inf")
        for child in state.get_children():
            value = max(value, minmaxAB(child, depth-1, alpha, beta, "black")[0])
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, None
    else:
        value = float("inf")
        for child in state.get_children():
            value = min(value, minmaxAB(child, depth-1, alpha, beta, "white")[0])
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, None