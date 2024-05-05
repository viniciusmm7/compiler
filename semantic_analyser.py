from abc import ABC, abstractmethod

DWORD: int = 4


class SymbolTable:
    def __init__(self) -> None:
        self.table: dict[str, tuple] = {}
        self.num_vars: int = 0

    def get(self, key: str) -> tuple:
        return self.table.get(key)

    def set(self, key: str, value: bool) -> int:
        if key not in self.table.keys():
            self.num_vars += 1
            ebp_diff: int = DWORD * self.num_vars
        else:
            st_tuple: tuple = self.table.get(key)
            ebp_diff: int = st_tuple[0]

        self.table[key] = (ebp_diff, value)
        return ebp_diff


class Node(ABC):
    i: int = 0

    def __init__(self, value: any, children: list) -> None:
        self.value: any = value
        self.children: list[Node | str] = children
        self.id: int = Node.new_id()

    @abstractmethod
    def evaluate(self, symbol_table: SymbolTable) -> str:
        pass

    @staticmethod
    def new_id() -> int:
        Node.i += 1
        return Node.i


class BinOp(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        left_node: Node = self.children[0]
        right_node: Node = self.children[1]

        left: str = left_node.evaluate(symbol_table)
        assembly = left
        assembly += 'PUSH EAX\n'

        right: str = right_node.evaluate(symbol_table)
        assembly += right
        assembly += 'MOV EBX, EAX\n'
        assembly += 'POP EAX\n'

        # if self.value == '..':
        #     return str(left) + str(right)

        if self.value == '+':
            assembly += 'ADD EAX, EBX\n'
            return assembly

        if self.value == '-':
            assembly += 'SUB EAX, EBX\n'
            return assembly

        if self.value == '*':
            assembly += 'IMUL EAX, EBX\n'
            return assembly

        if self.value == '/':
            # if right == 0:
            #     raise ZeroDivisionError('Division by zero')

            assembly += 'IDIV EBX\n'
            return assembly

        if self.value == 'and':
            assembly += 'AND EAX, EBX\n'
            return assembly

        if self.value == 'or':
            assembly += 'OR EAX, EBX\n'
            return assembly

        # if not isinstance(left, type(right)):
        #     raise TypeError(f'Cannot perform operation on "{type(left)}" and "{type(right)}"')

        assembly += 'CMP EAX, EBX\n'

        if self.value == '==':
            assembly += 'CALL binop_je\n'
            return assembly

        if self.value == '>':
            assembly += 'CALL binop_jg\n'
            return assembly

        if self.value == '<':
            assembly += 'CALL binop_jl\n'
            return assembly

        raise ValueError(f'Invalid operator "{self.value}"')


class UnOp(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        child_node: Node = self.children[0]
        child_value: str = child_node.evaluate(symbol_table)
        assembly = child_value

        if self.value == '+':
            return assembly

        if self.value == '-':
            assembly += 'NEG EAX\n'
            return assembly

        if self.value == 'not':
            assembly += 'NOT EAX\n'
            return assembly

        raise ValueError(f'Invalid operator "{self.value}"')


class IntVal(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        if not isinstance(self.value, int):
            raise ValueError(f'Invalid int value "{self.value}"')

        assembly = f'MOV EAX, {self.value}\n'

        return assembly


class StrVal(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        if not isinstance(self.value, str):
            raise ValueError(f'Invalid str value "{self.value}"')

        return self.value


class NoOp(Node):
    def evaluate(self, symbol_table: SymbolTable) -> None:
        pass


class IdentifierNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        key: str = self.value
        st_tuple: tuple = symbol_table.get(key)
        ebp_diff: int = st_tuple[0]
        # value: int = st_tuple[1]
        #
        # if value is None:
        #     raise ValueError(f'Undefined variable "{key}"')

        assembly = f'MOV EAX, [EBP-{ebp_diff}]\n'
        return assembly


class Assignment(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        key: str = self.children[0]
        value: str = self.children[1].evaluate(symbol_table)

        assembly = value

        # if not isinstance(value, (int, str)):
        #     raise ValueError(f'Invalid value "{value}"')

        if key not in symbol_table.table.keys():
            raise NameError(f'Undefined variable "{key}"')

        ebp_diff = symbol_table.set(key, True)
        assembly += f'MOV [EBP-{ebp_diff}], EAX\n'
        return assembly


class VarDeclaration(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        key: str = self.children[0]

        if key in symbol_table.table.keys():
            raise ValueError(f'Variable "{key}" already declared')

        assembly = 'PUSH DWORD 0\n'

        if self.children[1] is not None:
            value: str = self.children[1].evaluate(symbol_table)
            ebp_diff: int = symbol_table.set(key, True)
            assembly += value
            assembly += f'MOV [EBP-{ebp_diff}], EAX\n'
            return assembly

        _: int = symbol_table.set(key, False)
        return assembly


class PrintNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        result: str = self.children[0].evaluate(symbol_table)
        assembly = result
        assembly += 'PUSH EAX\n'
        assembly += 'PUSH formatout\n'
        assembly += 'CALL printf\n'
        assembly += 'ADD ESP, 8\n'
        return assembly


class BlockNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        assembly = ''

        for child in self.children:
            result: str = child.evaluate(symbol_table)
            if result is not None:
                assembly += result

        return assembly


class IfNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        condition: Node = self.children[0]
        block: Node = self.children[1]
        else_block: Node = self.children[2]

        assembly = condition.evaluate(symbol_table)
        assembly += 'CMP EAX, False\n'
        assembly += f'JE ELSE_{block.id}\n'
        assembly += block.evaluate(symbol_table)
        assembly += f'JMP EXIT_{block.id}\n'
        assembly += f'ELSE_{block.id}:\n'
        assembly += else_block.evaluate(symbol_table)
        assembly += f'EXIT_{block.id}:\n'

        return assembly


class WhileNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        condition: Node = self.children[0]
        block: Node = self.children[1]

        assembly = f'LOOP_{block.id}:\n'
        assembly += condition.evaluate(symbol_table)
        assembly += 'CMP EAX, False\n'
        assembly += f'JE EXIT_{block.id}\n'
        assembly += block.evaluate(symbol_table)
        assembly += f'JMP LOOP_{block.id}\n'
        assembly += f'EXIT_{block.id}:\n'

        return assembly


class ReadNode(Node):
    def evaluate(self, symbol_table: SymbolTable) -> str:
        assembly = 'PUSH scanint\n'
        assembly += 'PUSH formatin\n'
        assembly += 'CALL scanf\n'
        assembly += 'ADD ESP, 8\n'
        assembly += 'MOV EAX, DWORD [scanint]\n'
        return assembly


class SemanticAnalyser:
    @staticmethod
    def run(ast: Node, symbol_table: SymbolTable = SymbolTable()) -> any:
        result = ast.evaluate(symbol_table)

        st_tuples = symbol_table.table.values()

        for st_tuple in st_tuples:
            if not st_tuple[1]:
                raise ValueError(f'Variable "{st_tuple[0]}" not initialized')

        return result
