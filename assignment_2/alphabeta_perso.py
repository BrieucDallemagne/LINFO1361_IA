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
            self.children.append(c)
    
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
    
    if player == "white": # max
        value = -float("inf")
        for child in state.get_children():
            value = max(value, minmaxAB(child, depth-1, alpha, beta, "black")[0])
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, None
    else: #min
        value = float("inf")
        for child in state.get_children():
            value = min(value, minmaxAB(child, depth-1, alpha, beta, "white")[0])
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, None
    
    
if __name__ == "__main__":
    root = Node("white")
    
    sub = Node("white")
    
    left = Node("black")
    right = Node("black")
    
    left.add_child(Node("white", 3), Node("white", 0), Node("white", -3))
    right.add_child(Node("white", 5), Node("white", 11), Node("white", 7))
    
    sub.add_child(left, right)
    
    sub2 = Node("white")
    
    left = Node("white")
    right = Node("white")
    
    left.add_child(Node("black", 5), Node("black", -5))
    right.add_child(Node("black", 0), Node("black", -2))
    
    sub2.add_child(left, right)
    
    sub3 = Node("white")

    mid = Node("black")
    mid.add_child(Node("white", -12), Node("white", 7), -10)
    
    sub3.add_child(mid)
    
    master = Node("black")
    master.add_child(sub, sub2, sub3)
    
    # Middle part
    
    mid = Node("white")
    mid.add_child(Node("white", 1))
    
    sub = Node("black")
    sub.add_child(mid)
    
    sub2 = Node("black")
    
    left = Node("white")
    right = Node("white")
    
    left.add_child(Node("black", -5), Node("black", 0))
    right.add_child(Node("black", 0), Node("black", 0))
    
    sub2.add_child(left, right) 
    
    master2 = Node("black")
    
    master2.add_child(sub, sub2)
    
    # right part of the tree
    
    sub1 = Node("black")
    
    sub1.add_child(Node("white", -6), Node("white", 6))
    
    
    sub2 = Node("black")
    
    sub2.add_child(Node("white", 4), Node("white", 1), Node("white", 2))
    
    sub3 = Node("black")
    
    sub3.add_child(Node("white", -2))
    
    left = Node("white")
    
    left.add_child(sub1, sub2, sub3)
    
        
    sub1 = Node("black")
    
    sub1.add_child(Node("white", 3), Node("white", 7))
    
    
    sub2 = Node("black")
    
    sub2.add_child(Node("white", -3), Node("white", -6))
    
    right.add_child(sub1, sub2)
    
    master3 = Node("black")
    
    master3.add_child(left, right)
    
    root.add_child(master, master2, master3)