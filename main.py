from sys import argv
from syntax_analyser import Parser
from semantic_analyser import SemanticAnalyser, Node, SymbolTable


def main() -> None:
    with open(argv[1], 'r') as file:
        code = file.read()

    symbol_table: SymbolTable = SymbolTable()
    ast: Node = Parser.run(code, symbol_table)
    result: int = SemanticAnalyser.run(ast, symbol_table)


if __name__ == '__main__':
    main()
