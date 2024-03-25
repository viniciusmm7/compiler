# Compiler

![git status](http://3.129.230.99/svg/viniciusmm7/compiler/)

## Diagrama sintático:
![Imagem do diagrama sintático do compilador](diagrama_sintatico.png)

## EBNF:
```
BLOCK = {STATEMENT} ;
STATEMENT = (IDENTIFIER "=" EXPRESSION) | ("print" "(" EXPRESSION ")") "\n" ;
EXPRESSION = TERM {("+" | "-") TERM} ;
TERM = FACTOR {("*" | "/") FACTOR} ;
FACTOR = NUMBER | IDENTIFIER | ("+" | "-") FACTOR | "(" EXPRESSION ")" ;
IDENTIFIER = LETTER, {LETTER | DIGIT | "_"} ;
NUMBER = DIGIT, {DIGIT} ;
LETTER = "a".."z" | "A".."Z" ;
DIGIT = 0..9 ;
```
