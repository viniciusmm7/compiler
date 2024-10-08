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
    def evaluate(self, symbol_table: SymbolTable) -> any:
        left_node: Node = self.children[0]
        right_node: Node = self.children[1]

        left: any = left_node.evaluate(symbol_table)
        right: any = right_node.evaluate(symbol_table)

        if self.value == '+':
            return left + right

        if self.value == '-':
            return left - right

        if self.value == '*':
            return left * right

        if self.value == '/':
            return left // right

        if self.value == '==':
            return int(left == right)

        if self.value == '>':
            return int(left > right)

        if self.value == '<':
            return int(left < right)

        if self.value == 'and':
            return left and right

        if self.value == 'or':
            return left or right

        if self.value == '..':
            return str(left) + str(right)

        raise ValueError(f'Invalid operator "{self.value}"')


class UnOp(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        child_node: Node = self.children[0]
        child_value: int = child_node.evaluate(symbol_table)

        if self.value == '+':
            return child_value

        elif self.value == '-':
            return -child_value

        elif self.value == 'not':
            return not child_value

        raise ValueError(f'Invalid operator "{self.value}"')


class IntVal(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        if not isinstance(self.value, int):
            raise ValueError(f'Invalid value "{self.value}"')

        return self.value


class StrVal(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        if not isinstance(self.value, str):
            raise ValueError(f'Invalid value "{self.value}"')

        return self.value


class NoOp(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        pass


class IdentifierNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        key: str = self.value
        value: int = symbol_table.get(key)
        if value is None:
            raise ValueError(f'Undefined variable "{key}"')
        return value


class Assignment(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        key: str = self.children[0]
        value: int = self.children[1].evaluate(symbol_table)
        if not isinstance(value, (int, str)):
            raise ValueError(f'Invalid value "{value}"')
        symbol_table.set(key, value)
        return value


class VarDeclaration(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        key: str = self.children[0]
        value: any = self.children[1].evaluate(symbol_table) if self.children[1] is not None else None
        symbol_table.set(key, value)


class PrintNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        result: int = self.children[0].evaluate(symbol_table)
        print(result)
        return result


class BlockNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        for child in self.children:
            child.evaluate(symbol_table)


class IfNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        condition: Node = self.children[0]
        block: Node = self.children[1]
        else_block: Node = self.children[2]

        if condition.evaluate(symbol_table):
            block.evaluate(symbol_table)

        elif len(else_block.children) > 0:
            else_block.evaluate(symbol_table)


class WhileNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        condition: Node = self.children[0]
        block: Node = self.children[1]

        while condition.evaluate(symbol_table):
            block.evaluate(symbol_table)


class ReadNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> int:
        value: int = int(input())
        return value


class SemanticAnalyser:
    @staticmethod
    def run(ast: Node, symbol_table: SymbolTable = SymbolTable()) -> any:
        return ast.evaluate(symbol_table)
