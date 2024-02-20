from sys import argv


class LexicalError(Exception):
    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)


class Token:
    def __init__(self, type: str, value: str):
        self.type: str = type
        self.value: str = value


class Tokenizer:
    def __init__(self, source: str):
        self.source: str = source
        self.position: int = 0
        self.next: Token

    def select_next(self):
        while self.position <= len(self.source):
            if self.position == len(self.source):
                self.next = Token('EOF', '')
                self.position += 1
                return

            if self.source[self.position] == ' ':
                self.position += 1
                continue

            if self.source[self.position].isdigit():
                start = self.position
                
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                
                self.next = Token('INT', int(self.source[start:self.position]))
                return

            if self.source[self.position] == '+':
                self.next = Token('PLUS', '+')
                self.position += 1
                return

            if self.source[self.position] == '-':
                self.next = Token('MINUS', '-')
                self.position += 1
                return

            raise LexicalError(f'Invalid token "{self.source[self.position]}" at position {self.position}')


class Parser:
    @staticmethod
    def parse_expression(tokenizer: Tokenizer):
        if tokenizer.next.type != 'INT':
            raise SyntaxError('The expression must start with an int value')

        result = tokenizer.next.value

        while True:
            tokenizer.select_next()
            token = tokenizer.next

            if token.type == 'EOF':
                break

            tokenizer.select_next()

            if token.type in ['PLUS', 'MINUS'] and tokenizer.next.type == 'EOF':
                raise SyntaxError(f'The expression must end with an int value, it ended with "{token.value}"')

            if token.type == 'PLUS':
                if tokenizer.next.type != 'INT':
                    raise SyntaxError(f'Expected an integer, found "{tokenizer.next.value}"')
                
                result += tokenizer.next.value
            
            elif token.type == 'MINUS':
                if tokenizer.next.type != 'INT':
                    raise SyntaxError(f'Expected an integer, found "{tokenizer.next.value}"')
                
                result -= tokenizer.next.value
            
            else:
                raise SyntaxError(f'Invalid syntax at position {tokenizer.position}')
            
        return result

    @staticmethod
    def run(code: str):
        tokenizer: Tokenizer = Tokenizer(code)
        tokenizer.select_next()
        result = Parser.parse_expression(tokenizer)
        return result


if __name__ == '__main__':
    result = Parser.run(argv[1])
    print(result)
