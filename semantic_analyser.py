from data_structures import Node


class SemanticAnalyser:
    @staticmethod
    def run(ast: Node) -> int | ValueError:
        return ast.evaluate()
