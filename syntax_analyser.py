from lexical_analyser import Tokenizer, Token


class Parser:
    @staticmethod
    def parse_term(tokenizer: Tokenizer) -> int:
        if tokenizer.next.type != 'INT':
            raise SyntaxError(f'The expression must start with an int value, started with "{tokenizer.next.value}"')

        result = tokenizer.next.value
        tokenizer.select_next()

        while tokenizer.next.type in ('MULT', 'DIV'):
            token = tokenizer.next

            tokenizer.select_next()

            if token.type == 'MULT':
                if tokenizer.next.type != 'INT':
                    raise SyntaxError(f'Expected an integer, found "{tokenizer.next.value}"')
                
                result *= tokenizer.next.value
                tokenizer.select_next()
            
            elif token.type == 'DIV':
                if tokenizer.next.type != 'INT':
                    raise SyntaxError(f'Expected an integer, found "{tokenizer.next.value}"')
                
                if tokenizer.next.value == 0:
                    raise ZeroDivisionError('Division by zero')
                
                result //= tokenizer.next.value
                tokenizer.select_next()
            
        return result

    @staticmethod
    def parse_expression(tokenizer: Tokenizer) -> int:
        def __verify_errors(token: Token):
            if token.type in ('PLUS', 'MINUS') and tokenizer.next.type == 'EOF':
                raise SyntaxError(f'The expression must end with an int value, it ended with "{token.value}"')
            
            if token.type not in ('PLUS', 'MINUS'):
                raise SyntaxError(f'Expected an operator, found "{token.value}"')
            
            if tokenizer.next.type in ('PLUS', 'MINUS'):
                raise SyntaxError(f'Expected an integer, found "{tokenizer.next.value}"')
        
        result = Parser.parse_term(tokenizer)

        while True:
            if tokenizer.next.type == 'EOF':
                break
            
            token = tokenizer.next

            tokenizer.select_next()
            
            __verify_errors(token)

            if token.type == 'PLUS':
                if tokenizer.next.type != 'INT':
                    raise SyntaxError(f'Expected an integer, found "{tokenizer.next.value}"')
                
                result += Parser.parse_term(tokenizer)
            
            elif token.type == 'MINUS':
                if tokenizer.next.type != 'INT':
                    raise SyntaxError(f'Expected an integer, found "{tokenizer.next.value}"')
                
                result -= Parser.parse_term(tokenizer)
                
            else:
                raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')
        
        return result

    @staticmethod
    def run(code: str):
        if not code:
            raise ValueError('The code cannot be empty')
        
        tokenizer: Tokenizer = Tokenizer(code)
        tokenizer.select_next()
        result = Parser.parse_expression(tokenizer)
        print(result)
