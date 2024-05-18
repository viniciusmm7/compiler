from abc import ABC, abstractmethod


class SymbolTable:
    def __init__(self) -> None:
        self.table: dict[str, any] = {}

    def get(self, key: str) -> any:
        return self.table.get(key)

    def set(self, key: str, value: any) -> None:
        self.table[key] = value


class FuncTable:
    def __init__(self) -> None:
        self.table: dict[str, any] = {}

    def get(self, key: str) -> any:
        return self.table.get(key)

    def set(self, key: str, value: any) -> None:
        self.table[key] = value


func_table: FuncTable = FuncTable()


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

        if self.value == '..':
            return str(left) + str(right)

        if isinstance(left, int) and isinstance(right, int):
            if self.value == '+':
                return left + right

            if self.value == '-':
                return left - right

            if self.value == '*':
                return left * right

            if self.value == '/':
                if right == 0:
                    raise ZeroDivisionError('Division by zero')

                return left // right

        if self.value == 'and':
            return left and right

        if self.value == 'or':
            return left or right

        if not isinstance(left, type(right)):
            raise TypeError(f'Cannot perform operation on "{type(left)}" and "{type(right)}"')

        if self.value == '==':
            return int(left == right)

        if self.value == '>':
            return int(left > right)

        if self.value == '<':
            return int(left < right)

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

        if key not in symbol_table.table.keys():
            raise NameError(f'Undefined variable "{key}"')

        symbol_table.set(key, value)
        return value


class VarDeclaration(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        key: str = self.children[0]

        if key in symbol_table.table.keys():
            raise ValueError(f'Variable "{key}" already declared')

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


class FuncDec(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        identifier: str = self.children[0]

        if func_table.get(identifier) is not None:
            raise ValueError(f'Function "{identifier}" already declared')

        func_table.set(identifier, self)


class FuncCall(Node):
    def evaluate(self, symbol_table: SymbolTable) -> any:
        func_node: Node = func_table.get(self.value)
        if func_node is None:
            raise ValueError(f'Function "{self.value}" not declared')

        local_st: SymbolTable = SymbolTable()
        arguments: list[Node] = func_node.children[1:-1]

        if len(arguments) != len(self.children):
            raise ValueError(f'Function "{self.value}" expects {len(arguments)} arguments, got {len(self.children)}')

        for arg, value in zip(arguments, self.children):
            local_st.set(arg.children[0], value.evaluate(symbol_table))

        block: Node = func_node.children[-1]
        block.evaluate(local_st)

        return_node: Node = block.children[-2]

        if return_node.value is None:
            return None

        if return_node.value in func_table.table.keys():
            return func_table.get(return_node.value)

        return local_st.get(return_node.value)


class ReturnNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        expression: Node = self.children[0]
        symbol_table.set(self.value, expression.evaluate(symbol_table))


class SemanticAnalyser:
    @staticmethod
    def run(ast: Node, symbol_table: SymbolTable = SymbolTable()) -> any:
        return ast.evaluate(symbol_table)
