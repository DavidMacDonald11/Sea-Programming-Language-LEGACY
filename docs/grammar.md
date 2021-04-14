# Sea Language Grammar

- atom
    * INT|FLOAT|IDENTIFIER
    * LPAREN expression RPAREN
- power
    * atom (POW factor)*
- factor
    * (PLUS|MINUS) factor
    * power
- term
    * factor ((MUL|DIV) factor)*
- arithmetic_expression
    * term ((PLUS|MINUS) term)*
- comparison_expression
    * NOT comparison_expression
    * arithmetic_expresion ((EE|NE|LT|GT|LTE|GTE) arithmetic_expression)*
- boolean_and_expression
    * comparison_expression (AND comparison_expression)*
- expression
    * TYPE IDENTIFIER EQUALS expression
    * boolean_and_expression (OR boolean_and_expression)*
- if_expression
    * IF expression COLON (block|(expression (NEWLINE|EOF)))
    * (ELIF expression COLON (block|(expression (NEWLINE|EOF)))*
    * (ELSE COLON (block|(expression (NEWLINE|EOF))))?
- line
    * (INDENT)* (if_expression|expression) (NEWLINE|EOF)
- block
    * (line)*
