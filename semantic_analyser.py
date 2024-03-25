from data_structures import Node, SymbolTable


class SemanticAnalyser:
    @staticmethod
    def run(ast: Node, symbol_table: SymbolTable = SymbolTable()) -> int:
        return ast.evaluate(symbol_table)
