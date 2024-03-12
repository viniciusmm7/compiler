from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, value: any, children: list) -> None:
        self.value: any = value
        self.children: list[Node] = children
        

    @abstractmethod
    def evaluate(self):
        pass
    

class BinOp(Node):
    def evaluate(self) -> int:
        left_node: Node = self.children[0]
        right_node: Node = self.children[1]
        
        left: int = left_node.evaluate()
        right: int = right_node.evaluate()
        
        if self.value == '+':
            return left + right
        
        elif self.value == '-':
            return left - right
        
        elif self.value == '*':
            return left * right
        
        elif self.value == '/':
            return left // right
        
        raise ValueError(f'Invalid operator "{self.value}"')
    

class UnOp(Node):
    def evaluate(self) -> int:
        child_node: Node = self.children[0]
        child_value: int = child_node.evaluate()
        
        if self.value == '+':
            return child_value
        
        elif self.value == '-':
            return -child_value
        
        raise ValueError(f'Invalid operator "{self.value}"')


class IntVal(Node):
    def evaluate(self) -> int:
        if not isinstance(self.value, int):
            raise ValueError(f'Invalid value "{self.value}"')

        return self.value


class NoOp(Node):
    def evaluate(self) -> None:
        pass
