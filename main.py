from sys import argv
from syntax_analyser import Parser
from semantic_analyser import SemanticAnalyser, Node, SymbolTable


def main() -> None:
    with open(argv[1], 'r') as file:
        file_name = file.name.split('.')[0]
        code = file.read()

    symbol_table: SymbolTable = SymbolTable()
    parser: Parser = Parser()
    ast: Node = parser.run(code)
    result: str = SemanticAnalyser.run(ast, symbol_table)

    with open(f'{file_name}.asm', 'w') as file:
        with open('header.asm', 'r') as header:
            file.write(header.read())

        file.write(result)

        with open('footer.asm', 'r') as footer:
            file.write(footer.read())


if __name__ == '__main__':
    main()
