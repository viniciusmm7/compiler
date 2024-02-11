from sys import argv
from compiler import Compiler


if __name__ == '__main__':
    source_code = argv[1]
    compiler = Compiler(source_code)
    compiler.compile()
