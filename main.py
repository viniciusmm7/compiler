from sys import argv
from syntax_analyser import Parser


if __name__ == '__main__':
    Parser.run(argv[1])
