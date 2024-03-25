from abc import ABC, abstractmethod


class SymbolTable:
    def __init__(self) -> None:
        self.table: dict[str, any] = {}

    def get(self, key: str) -> any:
        return self.table.get(key)

    def set(self, key: str, value: any) -> None:
        self.table[key] = value


class Node(ABC):
    def __init__(self, value: any, children: list) -> None:
        self.value: any = value
        self.children: list[Node | str] = children

    @abstractmethod
    def evaluate(self, symbol_table: SymbolTable) -> any:
        pass


class BinOp(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        left_node: Node = self.children[0]
        right_node: Node = self.children[1]

        left: int = left_node.evaluate(symbol_table)
        right: int = right_node.evaluate(symbol_table)

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
    def evaluate(self, symbol_table: SymbolTable) -> int:
        child_node: Node = self.children[0]
        child_value: int = child_node.evaluate(symbol_table)

        if self.value == '+':
            return child_value

        elif self.value == '-':
            return -child_value

        raise ValueError(f'Invalid operator "{self.value}"')


class IntVal(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        if not isinstance(self.value, int):
            raise ValueError(f'Invalid value "{self.value}"')

        return self.value


class NoOp(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        pass


class IdentifierNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        key: str = self.value
        return symbol_table.get(key)


class Assignment(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        key: str = self.children[0]
        value: int = self.children[1].evaluate(symbol_table)
        symbol_table.set(key, value)
        return value


class PrintNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        result: int = self.children[0].evaluate(symbol_table)
        print(result)
        return result


class BlockNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        for child in self.children:
            child.evaluate(symbol_table)
