# Compiler

![git status](http://3.129.230.99/svg/viniciusmm7/compiler/)

## Diagrama sintático:
![Imagem do diagrama sintático do compilador](diagrama_sintatico.png)

## EBNF:
```
BLOCK = {STATEMENT} ;
STATEMENT = ( | (IDENTIFIER, "=", BOOL_EXPRESSION) | ("print", "(", BOOL_EXPRESSION, ")") | (("while", BOOL_EXPRESSION, "do", "\n", {STATEMENT}) | ("if", BOOL_EXPRESSION, "then", "\n", {STATEMENT}, (("else", {STATEMENT} | )))), "end"), "\n" ;
BOOL_EXPRESSION = BOOL_TERM, {"or", BOOL_TERM} ;
BOOL_TERM = RELATIONAL_EXPRESSION, {"and", RELATIONAL_EXPRESSION} ;
RELATIONAL_EXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION} ;
EXPRESSION = TERM, {("+" | "-"), TERM} ;
TERM = FACTOR, {("*" | "/"), FACTOR} ;
FACTOR = NUMBER | IDENTIFIER | ("+" | "-" | "not"), FACTOR | "(", BOOL_EXPRESSION, ")" | "read()" ;
IDENTIFIER = LETTER, {LETTER | DIGIT | "_"} ;
NUMBER = DIGIT, {DIGIT} ;
LETTER = "a".."z" | "A".."Z" ;
DIGIT = 0..9 ;
```
