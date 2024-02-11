import unittest
from compiler import Compiler


class TestCompiler(unittest.TestCase):
    # ----- Valid syntax
    def test_addition(self):
        compiler = Compiler('1+1')
        self.assertEqual(compiler.compile(show_result=False), 2)

    def test_subtraction(self):
        compiler = Compiler('1-1')
        self.assertEqual(compiler.compile(show_result=False), 0)
    
    def test_addition_subtraction(self):
        compiler = Compiler('1+1-1')
        self.assertEqual(compiler.compile(show_result=False), 1)
        
    def test_subtraction_addition(self):
        compiler = Compiler('1-1+1')
        self.assertEqual(compiler.compile(show_result=False), 1)
        
    def test_multiplication(self):
        compiler = Compiler('3*3')
        self.assertEqual(compiler.compile(show_result=False), 9)
    
    def test_division(self):
        compiler = Compiler('9/3')
        self.assertEqual(compiler.compile(show_result=False), 3)
        
    def test_add_sub_mul_div_1(self):
        compiler = Compiler('1-1+2*9/3')
        self.assertEqual(compiler.compile(show_result=False), 6)
        
    def test_add_sub_mul_div_2(self):
        compiler = Compiler('3*3-1+4/2')
        self.assertEqual(compiler.compile(show_result=False), 10)
        
    def test_valid_double_division(self):
        compiler = Compiler('27/3/3')
        self.assertEqual(compiler.compile(show_result=False), 3)
    
    def test_valid_syntax_spacing(self):
        compiler = Compiler('1 + 1')
        self.assertEqual(compiler.compile(show_result=False), 2)
    
    # ----- Invalid syntax
    def test_invalid_double_sign(self):
        invalid_expressions = ['1+-1', '1+*1', '1+/1', '1-*1', '1-/1', '1*/1']
        for expr in invalid_expressions:
            compiler = Compiler(expr)
            with self.assertRaises(SyntaxError):
                compiler.compile(show_result=False)
    
    def test_invalid_sign_only(self):
        invalid_expressions = ['+', '-', '*', '/']
        for expr in invalid_expressions:
            compiler = Compiler(expr)
            with self.assertRaises(SyntaxError):
                compiler.compile(show_result=False)

    def test_invalid_syntax_spacing(self):
        compiler = Compiler('1 1')
        with self.assertRaises(SyntaxError):
            compiler.compile(show_result=False)
            
    def test_invalid_syntax_start_with_operator(self):
        invalid_expressions = ['+1', '-1', '*1', '/1']
        for expr in invalid_expressions:
            compiler = Compiler(expr)
            with self.assertRaises(SyntaxError):
                compiler.compile(show_result=False)
            
    def test_invalid_syntax_end_with_operator(self):
        invalid_expressions = ['1+', '1-', '1*', '1/']
        for expr in invalid_expressions:
            compiler = Compiler(expr)
            with self.assertRaises(SyntaxError):
                compiler.compile(show_result=False)


if __name__ == '__main__':
    unittest.main()
