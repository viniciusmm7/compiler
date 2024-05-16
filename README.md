# Compiler

![git status](http://3.129.230.99/svg/viniciusmm7/compiler/)

## Diagrama sintático:
![Imagem do diagrama sintático do compilador](diagrama_sintatico.png)

## EBNF:
```
BLOCK = {STATEMENT} ;
STATEMENT = ( 
    | IDENTIFIER, "=", BOOL_EXPRESSION
    | "local", IDENTIFIER, ( | "=", BOOL_EXPRESSION)
    | "print", "(", BOOL_EXPRESSION, ")"
    | "return", BOOL_EXPRESSION
    | (
        "while", BOOL_EXPRESSION, "do", "\n", {STATEMENT}
        | "if", BOOL_EXPRESSION, "then", "\n", {STATEMENT}, (("else", {STATEMENT} | ))
        | "function", IDENTIFIER, "(", (IDENTIFIER, {",", IDENTIFIER}, | ), ")", "\n", {STATEMENT}
    ), "end"
), "\n" ;
BOOL_EXPRESSION = BOOL_TERM, {"or", BOOL_TERM} ;
BOOL_TERM = RELATIONAL_EXPRESSION, {"and", RELATIONAL_EXPRESSION} ;
RELATIONAL_EXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION} ;
EXPRESSION = TERM, {("+" | "-" | ".."), TERM} ;
TERM = FACTOR, {("*" | "/"), FACTOR} ;
FACTOR = NUMBER
    | STRING
    | IDENTIFIER
    | ("+" | "-" | "not"), FACTOR
    | "(", BOOL_EXPRESSION, ")"
    | "read()" ;

IDENTIFIER = LETTER, {LETTER | DIGIT | "_"} ;
NUMBER = DIGIT, {DIGIT} ;
STRING = '"', {CHARACTER}, '"' ;
CHARACTER = LETTER | DIGIT | SYMBOL | " " ;
LETTER = LOWERCASE | UPPERCASE ;
LOWERCASE = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" ;
UPPERCASE = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;
DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
SYMBOL = "!" | "@" | "#" | "$" | "%" | "&" | "*" | "(" | ")" | "-" | "+" | "=" | "[" | "]" | "{" | "}" | ";" | ":" | "," | "." | "<" | ">" | "/" | "?" | "|" | "\" | "'" | "`" | "~" | "^" | "_" ;
```
