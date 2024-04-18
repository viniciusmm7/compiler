from lexical_analyser import Tokenizer, PrePro
from semantic_analyser import *


class Parser:
    tokenizer = None

    @staticmethod
    def parse_factor() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer

        if tokenizer.next.type == 'INT':
            token = tokenizer.next.value
            tokenizer.select_next()
            return IntVal(token, [])

        if tokenizer.next.type == 'STRING':
            token = tokenizer.next.value
            tokenizer.select_next()
            return StrVal(token, [])

        elif tokenizer.next.type == 'IDENTIFIER':
            identifier = tokenizer.next.value
            tokenizer.select_next()
            return IdentifierNode(identifier, [])

        elif tokenizer.next.type in ['PLUS', 'MINUS', 'NOT']:
            token = tokenizer.next.value
            tokenizer.select_next()
            return UnOp(token, [Parser.parse_factor()])

        elif tokenizer.next.type == 'LPAREN':
            tokenizer.select_next()
            result: Node = Parser.parse_bool_expression()

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
    def parse_term() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer
        result: Node = Parser.parse_factor()

        while tokenizer.next.type in ['MULT', 'DIV']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_factor()])

        return result

    @staticmethod
    def parse_expression() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer
        result: Node = Parser.parse_term()

        while tokenizer.next.type in ['PLUS', 'MINUS', 'CONCAT']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_term()])

        return result
    
    @staticmethod
    def parse_relational_expression() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer
        result: Node = Parser.parse_expression()
        
        while tokenizer.next.type in ['EQUAL', 'GREATERTHAN', 'LESSTHAN']:
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_expression()])

        return result
    
    @staticmethod
    def parse_bool_term() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer
        result: Node = Parser.parse_relational_expression()

        while tokenizer.next.type == 'AND':
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_relational_expression()])

        return result

    @staticmethod
    def parse_bool_expression() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer
        result: Node = Parser.parse_bool_term()
        
        while tokenizer.next.type == 'OR':
            token = tokenizer.next.value
            tokenizer.select_next()
            result = BinOp(token, [result, Parser.parse_bool_term()])
            
        return result

    @staticmethod
    def parse_statement() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer
        if tokenizer.next.type == 'NEWLINE':
            tokenizer.select_next()
            return NoOp(None, [])

        elif tokenizer.next.type == 'IDENTIFIER':
            identifier = tokenizer.next.value
            tokenizer.select_next()

            if tokenizer.next.type == 'ASSIGN':
                assignment_token = tokenizer.next.value
                tokenizer.select_next()
                expression = Parser.parse_bool_expression()

                if tokenizer.next.type in ['NEWLINE', 'EOF']:
                    return Assignment(assignment_token, [identifier, expression])

                raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

            raise SyntaxError(f'"{identifier}" is missing assignment operator at position "{tokenizer.position}"')

        elif tokenizer.next.type == 'LOCAL':
            tokenizer.select_next()

            if tokenizer.next.type == 'IDENTIFIER':
                identifier = tokenizer.next.value
                tokenizer.select_next()
                expression = None

                if tokenizer.next.type == 'ASSIGN':
                    tokenizer.select_next()
                    expression = Parser.parse_bool_expression()

                if tokenizer.next.type in ['NEWLINE', 'EOF']:
                    return VarDeclaration('LOCAL', [identifier, expression])

                raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

        elif tokenizer.next.type == 'PRINT':
            token = tokenizer.next.value
            tokenizer.select_next()

            if tokenizer.next.type == 'LPAREN':
                tokenizer.select_next()
                expression = Parser.parse_bool_expression()

                if tokenizer.next.type == 'RPAREN':
                    tokenizer.select_next()

                    if tokenizer.next.type in ['NEWLINE', 'EOF']:
                        return PrintNode(token, [expression])

                    raise SyntaxError(f'Invalid syntax at position "{tokenizer.position}"')

                raise SyntaxError(f'Missing right parenthesis when calling print() at position "{tokenizer.position}"')

            raise SyntaxError(f'Missing parenthesis when calling print() at position "{tokenizer.position}"')
                    
        elif tokenizer.next.type == 'IF':
            tokenizer.select_next()
            condition = Parser.parse_bool_expression()
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
                        if_statement = Parser.parse_statement()
                        if_node.children[1].children.append(if_statement)

                        if tokenizer.next.type not in ['END', 'ELSE']:
                            tokenizer.select_next()

                    if tokenizer.next.type == 'ELSE':
                        tokenizer.select_next()

                        if tokenizer.next.type == 'NEWLINE':
                            tokenizer.select_next()

                            while tokenizer.next.type != 'END':
                                else_statement = Parser.parse_statement()
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
            condition = Parser.parse_bool_expression()
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
                        statement = Parser.parse_statement()
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
    def parse_block() -> Node:
        tokenizer: Tokenizer = Parser.tokenizer
        result = BlockNode('BLOCK', [])

        while tokenizer.next.type != 'EOF':
            result.children.append(Parser.parse_statement())

        return result

    @staticmethod
    def run(code: str) -> Node:
        if not code:
            raise ValueError('The code cannot be empty')

        code = PrePro.filter(code)

        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.select_next()

        result = Parser.parse_block()

        if Parser.tokenizer.next.type != 'EOF':
            raise SyntaxError(f'Invalid syntax at position "{Parser.tokenizer.position}"')

        return result
