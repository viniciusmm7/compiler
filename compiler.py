from lexical_analyser import LexicalAnalyser
from syntax_analyser import SyntaxAnalyser
from semantic_analyser import SemanticAnalyzer


class Compiler:
    def __init__(self, source_code: str):
        self.source_code: str = source_code

    def compile(self, show_result=True):
        lexical_analyser = LexicalAnalyser(self.source_code)
        tokens = lexical_analyser.tokenize()
        
        syntax_analyser = SyntaxAnalyser(tokens)
        tree = syntax_analyser.make_tree()
        
        semantic_analyser = SemanticAnalyzer(tree)
        result = semantic_analyser.evaluate()
        
        if show_result:
            print(result)
            
        return result
