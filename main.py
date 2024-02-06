from sys import argv
from re import findall


class Compiler:
    MINUS = '-'
    PLUS = '+'
    
    def __init__(self, input_op: str):
        self.input_op: str = input_op
        self.tokens: list = []
        self.tree = None
        self.result = None
        
    def __tokenize(self):
        self.tokens = findall(r'\d+|\D', self.input_op)
        self.tokens = [token.strip() for token in self.tokens if token.strip()]
        
    def __check_syntax(self):
        starts_with_operator = self.tokens[0] in [self.MINUS, self.PLUS]
        ends_with_operator = self.tokens[-1] in [self.MINUS, self.PLUS]

        if starts_with_operator or ends_with_operator:
            raise SyntaxError("Invalid expression: expression cannot start or end with an operator")

        for i in range(len(self.tokens)-1):
            current_is_operator = self.tokens[i] in [self.MINUS, self.PLUS]
            next_is_operator = self.tokens[i+1] in [self.MINUS, self.PLUS]

            if not (current_is_operator or next_is_operator):
                raise SyntaxError("Invalid expression: operators are required between numbers")

            elif current_is_operator and next_is_operator:
                raise SyntaxError("Invalid expression: two operators cannot appear consecutively")
            
    def __check_semantics(self):
        pass
    
    def __evaluate(self):
        result = int(self.tokens[0])
        operator = None

        for token in self.tokens:
            if token in [self.MINUS, self.PLUS]:
                operator = token
            else:
                if operator == self.MINUS:
                    result -= int(token)
                elif operator == self.PLUS:
                    result += int(token)

        self.result = result
        
    def compile(self, show_result=True):
        self.__tokenize()
        self.__check_syntax()
        self.__check_semantics()
        self.__evaluate()
        if show_result:
            print(self.result)


if __name__ == '__main__':
    input_op = argv[1]
    compiler = Compiler(input_op)
    compiler.compile()
