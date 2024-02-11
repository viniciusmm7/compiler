from signs import SIGNS


class SyntaxAnalyser:
    def __init__(self, tokens: list[str]):
        self.tokens: list[str] = tokens

    def __check_syntax(self):
        starts_with_operator = self.tokens[0] in SIGNS
        ends_with_operator = self.tokens[-1] in SIGNS

        if starts_with_operator or ends_with_operator:
            raise SyntaxError("Invalid expression: expression cannot start or end with an operator")

        for i in range(len(self.tokens) - 1):
            current_is_operator = self.tokens[i] in SIGNS
            next_is_operator = self.tokens[i + 1] in SIGNS

            if not (current_is_operator or next_is_operator):
                raise SyntaxError("Invalid expression: operators are required between numbers")

            elif current_is_operator and next_is_operator:
                raise SyntaxError("Invalid expression: two operators cannot appear consecutively")
    
    def make_tree(self):
        # TODO: Implement it correctly
        self.__check_syntax()
        return self.tokens
