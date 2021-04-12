# Sea Language Grammar

- line
    * (INDENT)* expression (NEWLINE|EOF)
- expression
    * TYPE IDENTIFIER EQUALS expression
    * boolean_and_expression (OR boolean_and_expression)*
- boolean_and_expression
    * comparison_expression (AND comparison_expression)*
- comparison_expression
    * NOT comparison_expression
    * arithmetic_expresion ((EE|LT|GT|LTE|GTE) arithmetic_expression)*
- arithmetic_expression
    * term ((PLUS|MINUS) term)*
- term
    * factor ((MUL|DIV) factor)*
- factor
    * (PLUS|MINUS) factor
    * power
- power
    * atom (POW factor)*
- atom
    * INT|FLOAT|IDENTIFIER
    * LPAREN expression RPAREN
    * if_expression
- if_expression
    * IF expression COLON ((NEWLINE block)|expression)
    * (ELIF expression COLON ((NEWLINE block)|expression)*
    * (ELSE ((NEWLINE block)|expression))?
