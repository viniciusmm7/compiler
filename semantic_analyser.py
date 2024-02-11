from signs import Sign, SIGNS
# from data_structures import Tree


class SemanticAnalyzer:
    def __init__(self, tree: list[str]):
        # REMEMBER: It's not a real tree, it's just a list of tokens.
        # TODO: Implement a real tree data structure.
        self.tree: list[str] = tree

    def __check_semantics(self):
        pass

    def evaluate(self):
        def precedence(operand: str):
            if operand in [Sign.MULTIPLICATION.value, Sign.DIVISION.value]:
                return 2
            elif operand in [Sign.MINUS.value, Sign.PLUS.value]:
                return 1
            return 0
        
        def apply_operator(operators: list, values: list):
            operator = operators.pop()
            right_operand = values.pop()
            left_operand = values.pop()
            
            if operator == Sign.MINUS.value:
                values.append(left_operand - right_operand)
            elif operator == Sign.PLUS.value:
                values.append(left_operand + right_operand)
            elif operator == Sign.MULTIPLICATION.value:
                values.append(left_operand * right_operand)
            elif operator == Sign.DIVISION.value:
                values.append(left_operand / right_operand)
        
        # TODO: Implement stack data structure if possible/necessary, maybe Python's list structure is a stack already.
        operators = [] # Simulating a stack
        values = [] # Simulating a stack

        for node in self.tree:
            if node.isdigit():
                values.append(int(node))
            elif node in SIGNS:
                while (operators and precedence(operators[-1]) >= precedence(node)):
                    apply_operator(operators, values)
                operators.append(node)

        while operators:
            apply_operator(operators, values)

        return values[0]
