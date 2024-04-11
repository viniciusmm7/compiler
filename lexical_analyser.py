from re import sub


class LexicalError(Exception):
    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)


class PrePro:
    @staticmethod
    def filter(source: str) -> str:
        source = sub(r'--.*?(?=\n|$)', '', source)
        return source


class Token:
    def __init__(self, token_type: str, value: any):
        self.type: str = token_type
        self.value: any = value


class Tokenizer:
    def __init__(self, source: str):
        self.source: str = source
        self.position: int = 0
        self.next: Token | None = None
        self.keywords: set[str] = {
            'print',
            'or',
            'and',
            'while',
            'do',
            'end',
            'if',
            'then',
            'else',
            'not',
            'read',
            }

    def select_next(self) -> None:
        while self.position <= len(self.source):
            if self.position == len(self.source):
                self.next = Token('EOF', '')
                self.position += 1
                return

            if self.source[self.position] in [' ', '\t']:
                self.position += 1
                continue

            if self.source[self.position].isalpha():
                start = self.position

                while self.position < len(self.source) and (
                        self.source[self.position].isalnum() or self.source[self.position] == '_'):
                    self.position += 1

                token_value: str = self.source[start:self.position]

                if token_value in self.keywords:
                    self.next = Token(token_value.upper(), token_value)

                else:
                    self.next = Token('IDENTIFIER', token_value)

                return

            if self.source[self.position].isdigit():
                start = self.position

                while True:
                    self.position += 1
                    if self.source[self.position].isalpha():
                        raise LexicalError(f'Invalid token "{self.source[self.position]}" at position {self.position}')
                    if self.position < len(self.source) and not self.source[self.position].isdigit():
                        break

                self.next = Token('INT', int(self.source[start:self.position]))
                return

            if self.source[self.position] == '=':
                if self.source[self.position + 1] == '=':
                    self.next = Token('EQUAL', '==')
                    self.position += 2
                    return

                self.next = Token('ASSIGN', '=')
                self.position += 1
                return
            
            if self.source[self.position] == '+':
                self.next = Token('PLUS', '+')
                self.position += 1
                return

            if self.source[self.position] == '-':
                self.next = Token('MINUS', '-')
                self.position += 1
                return

            if self.source[self.position] == '*':
                self.next = Token('MULT', '*')
                self.position += 1
                return

            if self.source[self.position] == '/':
                self.next = Token('DIV', '/')
                self.position += 1
                return

            if self.source[self.position] == '(':
                self.next = Token('LPAREN', '(')
                self.position += 1
                return

            if self.source[self.position] == ')':
                self.next = Token('RPAREN', ')')
                self.position += 1
                return

            if self.source[self.position] == '>':
                self.next = Token('GREATERTHAN', '>')
                self.position += 1
                return
            
            if self.source[self.position] == '<':
                self.next = Token('LESSTHAN', '<')
                self.position += 1
                return

            if self.source[self.position] == '\n':
                self.next = Token('NEWLINE', '\n')
                self.position += 1
                return

            raise LexicalError(f'Invalid token "{self.source[self.position]}" at position {self.position}')
