from lexical_analyser import Tokenizer, PrePro
from semantic_analyser import *


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
            return IdentifierNode(identifier, [])

        elif tokenizer.next.type in ['PLUS', 'MINUS', 'NOT']:
            token = tokenizer.next.value
            tokenizer.select_next()
            return UnOp(token, [Parser.parse_factor(tokenizer, symbol_table)])

        elif tokenizer.next.type == 'LPAREN':
            tokenizer.select_next()
            result: Node = Parser.parse_bool_expression(tokenizer, symbol_table)

            if tokenizer.next.type == 'RPAREN':
                tokenizer.select_next()
                return result

            raise SyntaxError(f'Missing closing parenthesis at position "{tokenizer.position}"')

        elif tokenizer.next.type == 'READ':
            tokenizer.select_next()

            if tokenizer.next.type == 'LPAREN':
                tokenizer.select_next()

                if tokenizer.next.type == 'RPAREN':
                    tokenizer.select_next()
                    return ReadNode('READ', [])

                raise SyntaxError(f'Missing closing parenthesis when calling read() at position "{tokenizer.position}"')

            raise SyntaxError(f'Invalid syntax calling read() at position "{tokenizer.position}"')

        elif tokenizer.next.type == 'NEWLINE':
            return NoOp(None, [])

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
    def parse_relational_expression(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        result: Node = Parser.parse_expression(tokenizer, symbol_table)
        
        while tokenizer.next.type in ['EQUAL', 'GREATERTHAN', 'LESSTHAN']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_expression(tokenizer, symbol_table)])

        return result
    
    @staticmethod
    def parse_bool_term(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        result: Node = Parser.parse_relational_expression(tokenizer, symbol_table)

        while tokenizer.next.type == 'AND':
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_relational_expression(tokenizer, symbol_table)])

        return result

    @staticmethod
    def parse_bool_expression(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        result: Node = Parser.parse_bool_term(tokenizer, symbol_table)
        
        while tokenizer.next.type == 'OR':
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_bool_term(tokenizer, symbol_table)])
            
        return result

    @staticmethod
    def parse_statement(tokenizer: Tokenizer, symbol_table: SymbolTable) -> Node:
        if tokenizer.next.type == 'NEWLINE':
            tokenizer.select_next()
            return NoOp(None, [])

        elif tokenizer.next.type == 'IDENTIFIER':
            identifier = tokenizer.next.value
            tokenizer.select_next()

            if tokenizer.next.type == 'ASSIGN':
                assignment_token = tokenizer.next.value
                tokenizer.select_next()
                expression = Parser.parse_bool_expression(tokenizer, symbol_table)

                if tokenizer.next.type in ['NEWLINE', 'EOF']:
                    return Assignment(assignment_token, [identifier, expression])

                raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

            raise SyntaxError(f'"{identifier}" is missing assignment operator at position "{tokenizer.position}"')

        elif tokenizer.next.type == 'PRINT':
            token = tokenizer.next.value
            tokenizer.select_next()

            if tokenizer.next.type == 'LPAREN':
                tokenizer.select_next()
                expression = Parser.parse_bool_expression(tokenizer, symbol_table)

                if tokenizer.next.type == 'RPAREN':
                    tokenizer.select_next()

                    if tokenizer.next.type in ['NEWLINE', 'EOF']:
                        return PrintNode(token, [expression])

                    raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

                raise SyntaxError(f'Missing right parenthesis when calling print() at position "{tokenizer.position}"')

            raise SyntaxError(f'Missing parenthesis when calling print() at position "{tokenizer.position}"')
                    
        elif tokenizer.next.type == 'IF':
            tokenizer.select_next()
            condition = Parser.parse_bool_expression(tokenizer, symbol_table)
            children = [
                condition,
                BlockNode('IF_BLOCK', []),
                BlockNode('ELSE_BLOCK', [])
            ]
            if_node = IfNode('IF', children)

            if tokenizer.next.type == 'THEN':
                tokenizer.select_next()

                if tokenizer.next.type == 'NEWLINE':
                    tokenizer.select_next()

                    while tokenizer.next.type not in ['END', 'ELSE']:
                        if_statement = Parser.parse_statement(tokenizer, symbol_table)
                        if_node.children[1].children.append(if_statement)

                        if tokenizer.next.type not in ['END', 'ELSE']:
                            tokenizer.select_next()

                    if tokenizer.next.type == 'ELSE':
                        tokenizer.select_next()

                        if tokenizer.next.type == 'NEWLINE':
                            tokenizer.select_next()

                            while tokenizer.next.type != 'END':
                                else_statement = Parser.parse_statement(tokenizer, symbol_table)
                                if_node.children[2].children.append(else_statement)
                                tokenizer.select_next()

                        else:
                            raise SyntaxError(f'Must have a line break after "else" at position "{tokenizer.position}"')

                    if tokenizer.next.type == 'END':
                        tokenizer.select_next()

                        if tokenizer.next.type in ['NEWLINE', 'EOF']:
                            return if_node

                    raise SyntaxError(f'If statement must terminate with "end" at position "{tokenizer.position}"')

                raise SyntaxError(f'Must have a line break after "then" at position "{tokenizer.position}"')

            raise SyntaxError(f'Expected "then" at position "{tokenizer.position}", found "{tokenizer.next.value}"')

        elif tokenizer.next.type == 'WHILE':
            tokenizer.select_next()
            condition = Parser.parse_bool_expression(tokenizer, symbol_table)
            children = [
                condition,
                BlockNode('WHILE_BLOCK', [])
            ]
            while_node = WhileNode('WHILE', children)

            if tokenizer.next.type == 'DO':
                tokenizer.select_next()

                if tokenizer.next.type == 'NEWLINE':
                    tokenizer.select_next()

                    while tokenizer.next.type != 'END':
                        statement = Parser.parse_statement(tokenizer, symbol_table)
                        while_node.children[1].children.append(statement)
                        tokenizer.select_next()

                    if tokenizer.next.type == 'END':
                        tokenizer.select_next()

                        if tokenizer.next.type in ['NEWLINE', 'EOF']:
                            return while_node

                    raise SyntaxError(f'While statement must terminate with "end" at position "{tokenizer.position}"')

                raise SyntaxError(f'Must have a line break after "do" at position "{tokenizer.position}"')

            raise SyntaxError(f'Expected "do" at position "{tokenizer.position}", found "{tokenizer.next.value}"')

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
