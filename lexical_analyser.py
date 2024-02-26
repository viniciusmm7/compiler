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
            
            if self.source[self.position] == '*':
                self.next = Token('MULT', '*')
                self.position += 1
                return
            
            if self.source[self.position] == '/':
                self.next = Token('DIV', '/')
                self.position += 1
                return

            raise LexicalError(f'Invalid token "{self.source[self.position]}" at position {self.position}')
