from lexical_analyser import Tokenizer


class Parser:
    @staticmethod
    def parse_factor(tokenizer: Tokenizer) -> int:
        if tokenizer.next.type == 'INT':
            result = tokenizer.next.value
            tokenizer.select_next()
            return result
        
        elif tokenizer.next.type == 'PLUS':
            tokenizer.select_next()
            return Parser.parse_factor(tokenizer)
        
        elif tokenizer.next.type == 'MINUS':
            tokenizer.select_next()
            return -Parser.parse_factor(tokenizer)
        
        elif tokenizer.next.type == 'LPAREN':
            tokenizer.select_next()
            result = Parser.parse_expression(tokenizer)
            
            if tokenizer.next.type != 'RPAREN':
                raise SyntaxError(f'Missing closing parenthesis at position "{tokenizer.position}"')
            
            tokenizer.select_next()
            return result

        else:
            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')
            
    
    @staticmethod
    def parse_term(tokenizer: Tokenizer) -> int:
        result = Parser.parse_factor(tokenizer)
        
        while tokenizer.next.type in ['MULT', 'DIV']:
            if tokenizer.next.type == 'MULT':
                tokenizer.select_next()
                result *= Parser.parse_factor(tokenizer)
                
            elif tokenizer.next.type == 'DIV':
                tokenizer.select_next()
                result //= Parser.parse_factor(tokenizer)
            
        return result


    @staticmethod
    def parse_expression(tokenizer: Tokenizer) -> int:
        result = Parser.parse_term(tokenizer)
        
        while tokenizer.next.type in ['PLUS', 'MINUS']:
            if tokenizer.next.type == 'PLUS':
                tokenizer.select_next()
                result += Parser.parse_term(tokenizer)
                
            elif tokenizer.next.type == 'MINUS':
                tokenizer.select_next()
                result -= Parser.parse_term(tokenizer)
            
        return result

    @staticmethod
    def run(code: str):
        if not code:
            raise ValueError('The code cannot be empty')
        
        tokenizer: Tokenizer = Tokenizer(code)
        tokenizer.select_next()
        result = Parser.parse_expression(tokenizer)
        
        if tokenizer.next.type != 'EOF':
            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')
        
        print(result)
