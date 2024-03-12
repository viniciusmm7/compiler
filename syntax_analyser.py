from lexical_analyser import Tokenizer, PrePro
from data_structures import Node, BinOp, UnOp, IntVal


class Parser:
    @staticmethod
    def parse_factor(tokenizer: Tokenizer) -> Node:
        if tokenizer.next.type == 'INT':
            token = tokenizer.next.value
            tokenizer.select_next()
            return IntVal(token, [])
        
        elif tokenizer.next.type == 'PLUS' or tokenizer.next.type == 'MINUS':
            token = tokenizer.next.value
            tokenizer.select_next()
            return UnOp(token, [Parser.parse_factor(tokenizer)])
        
        elif tokenizer.next.type == 'LPAREN':
            tokenizer.select_next()
            result: Node = Parser.parse_expression(tokenizer)
            
            if tokenizer.next.type != 'RPAREN':
                raise SyntaxError(f'Missing closing parenthesis at position "{tokenizer.position}"')
            
            tokenizer.select_next()
            return result

        else:
            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')
            
    
    @staticmethod
    def parse_term(tokenizer: Tokenizer) -> Node:
        result: Node = Parser.parse_factor(tokenizer)
        
        while tokenizer.next.type in ['MULT', 'DIV']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_factor(tokenizer)])
            
        return result


    @staticmethod
    def parse_expression(tokenizer: Tokenizer) -> Node:
        result: Node = Parser.parse_term(tokenizer)
        
        while tokenizer.next.type in ['PLUS', 'MINUS']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_term(tokenizer)])
            
        return result


    @staticmethod
    def run(code: str) -> Node:
        if not code:
            raise ValueError('The code cannot be empty')
        
        code = PrePro.filter(code)
        
        tokenizer: Tokenizer = Tokenizer(code)
        tokenizer.select_next()
        
        result = Parser.parse_expression(tokenizer)
        
        if tokenizer.next.type != 'EOF':
            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')
        
        return result
