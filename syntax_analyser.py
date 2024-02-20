from lexical_analyser import Tokenizer


class Parser:
    @staticmethod
    def parse_expression(tokenizer: Tokenizer) -> int:
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
    def run(code: str) -> None:
        tokenizer: Tokenizer = Tokenizer(code)
        tokenizer.select_next()
        result = Parser.parse_expression(tokenizer)
        print(result)
