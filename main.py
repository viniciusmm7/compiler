from sys import argv
from syntax_analyser import Parser
from semantic_analyser import SemanticAnalyser


def main() -> None:
    with open(argv[1], 'r') as file:
        code = file.read()

    ast = Parser.run(code)
    result = SemanticAnalyser.run(ast)
    print(f'Resultado: {result}')


if __name__ == '__main__':
    main()
