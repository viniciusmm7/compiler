from lexical_analyser import Tokenizer, PrePro
from data_structures import Node, BinOp, UnOp, IntVal, NoOp, Assignment, PrintNode, BlockNode, SymbolTable


class Parser:
    @staticmethod
    def parse_factor(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        if tokenizer.next.type == 'INT':
            token = tokenizer.next.value
            tokenizer.select_next()
            return IntVal(token, [])

        elif tokenizer.next.type == 'IDENTIFIER':
            identifier = tokenizer.next.value
            tokenizer.select_next()

            if tokenizer.next.type == 'ASSIGN':
                assignment_token = tokenizer.next.value
                tokenizer.select_next()
                expression = Parser.parse_expression(tokenizer, symbol_table)
                return Assignment(assignment_token, [identifier, expression])

        elif tokenizer.next.type == 'PLUS' or tokenizer.next.type == 'MINUS':
            token = tokenizer.next.value
            tokenizer.select_next()
            return UnOp(token, [Parser.parse_factor(tokenizer, symbol_table)])

        elif tokenizer.next.type == 'LPAREN':
            tokenizer.select_next()
            result: Node = Parser.parse_expression(tokenizer, symbol_table)

            if tokenizer.next.type != 'RPAREN':
                raise SyntaxError(f'Missing closing parenthesis at position "{tokenizer.position}"')

            tokenizer.select_next()
            return result

        else:
            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

    @staticmethod
    def parse_term(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        result: Node = Parser.parse_factor(tokenizer, symbol_table)

        while tokenizer.next.type in ['MULT', 'DIV']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_factor(tokenizer, symbol_table)])

        return result

    @staticmethod
    def parse_expression(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        result: Node = Parser.parse_term(tokenizer, symbol_table)

        while tokenizer.next.type in ['PLUS', 'MINUS']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_term(tokenizer, symbol_table)])

        return result

    @staticmethod
    def parse_statement(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        if tokenizer.next.type == 'NEWLINE':
            token = tokenizer.next.value
            tokenizer.select_next()
            return NoOp(token, [])

        if tokenizer.next.type == 'IDENTIFIER':
            identifier = tokenizer.next.value
            tokenizer.select_next()

            if tokenizer.next.type == 'ASSIGN':
                assignment_token = tokenizer.next.value
                tokenizer.select_next()
                expression = Parser.parse_expression(tokenizer, symbol_table)

                if tokenizer.next.type == 'NEWLINE':
                    tokenizer.select_next()
                    return Assignment(assignment_token, [identifier, expression])

                raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

        if tokenizer.next.type == 'PRINT':
            token = tokenizer.next.value
            tokenizer.select_next()

            if tokenizer.next.type == 'LPAREN':
                tokenizer.select_next()
                expression = Parser.parse_expression(tokenizer, symbol_table)

                if tokenizer.next.type == 'RPAREN':
                    tokenizer.select_next()

                    if tokenizer.next.type == 'NEWLINE' or tokenizer.next.type == 'EOF':
                        tokenizer.select_next()
                        return PrintNode(token, [expression])

                    raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

                raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

    @staticmethod
    def parse_block(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        result = BlockNode('BLOCK', [])

        while tokenizer.next.type != 'EOF':
            result.children.append(Parser.parse_statement(tokenizer, symbol_table))

        return result

    @staticmethod
    def run(code: str, symbol_table: SymbolTable) -> Node:
        if not code:
            raise ValueError('The code cannot be empty')

        code = PrePro.filter(code)

        tokenizer: Tokenizer = Tokenizer(code)
        tokenizer.select_next()

        result = Parser.parse_block(tokenizer, symbol_table)

        if tokenizer.next.type != 'EOF':
            raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

        return result
