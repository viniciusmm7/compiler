# Compiler

![git status](http://3.129.230.99/svg/viniciusmm7/compiler/)

## Diagrama sintático:
![Imagem do diagrama sintático do compilador](diagrama_sintatico.png)

## EBNF:
```
EXPRESSION = TERM, {("+" | "-"), TERM} ;
TERM = FACTOR, {("*" | "/"), FACTOR} ;
FACTOR = NUMBER | ("+" | "-") FACTOR | "(" EXPRESSION ")" ;
NUMBER = DIGIT, {DIGIT} ;
DIGIT = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ;
```
