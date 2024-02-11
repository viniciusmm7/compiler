class Node:
    def __init__(self, data):
        self.data = data # Should be a grammar rule from BNF grammar
        self.left = None
        self.right = None
    

class Tree:
    def __init__(self):
        self.root: Node = None
