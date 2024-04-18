from sys import argv
from syntax_analyser import Parser
from semantic_analyser import SemanticAnalyser, Node, SymbolTable


def main() -> None:
    with open(argv[1], 'r') as file:
        code = file.read()

    symbol_table: SymbolTable = SymbolTable()
    parser: Parser = Parser()
    ast: Node = parser.run(code)
    result: any = SemanticAnalyser.run(ast, symbol_table)
    if None in symbol_table.table.values():
        raise ValueError('Variable declared but not initialized')


if __name__ == '__main__':
    main()
