# Sea Language Grammar

- atom
    * INT|FLOAT|IDENTIFIER
    * LPAREN expression RPAREN
- power
    * atom (POW factor)*
- factor
    * (PLUS|MINUS|BIT_NOT) factor
    * power
- term
    * factor ((MUL|DIV|MOD) factor)*
- arithmetic_expression
    * term ((PLUS|MINUS) term)*
- bitwise_shift_expression
    * arithmetic_expression (LSHIFT|RSHIFT) arithmetic_expression)*
- bitwise_and_expression
    * bitwise_shift_expression (BIT_AND bitwise_shift_expression)*
- bitwise_xor_expression
    * bitwise_and_expression (BIT_XOR bitwise_and_expression)*
- bitwise_or_expression
    * bitwise_xor_expression (BIT_OR bitwise_xor_expression)*
- comparison_expression
    * bitwise_or_expression ((EE|NE|LT|GT|LTE|GTE) bitwise_or_expression)*
- boolean_not_expression
    * ((NOT boolean_not_expression)|comparison_expression)
- boolean_and_expression
    * boolean_not_expression (AND boolean_not_expression)*
- boolean_xor_expression
    * boolean_and_expression (XOR boolean_and_expression)*
- boolean_or_expression
    * boolean_xor_expression (OR boolean_xor_expression)*
- expression
    * boolean_or_expression IF boolean_or_expression ELSE boolean_or_expression
    * TYPE IDENTIFIER EQUALS expression
- if_expression
    * IF expression COLON (block|(expression (NEWLINE|EOF)))
    * (ELIF expression COLON (block|(expression (NEWLINE|EOF)))*
    * (ELSE COLON (block|(expression (NEWLINE|EOF))))?
- line
    * EOF
    * NEWLINE
    * (INDENT)* REDEFINE IDENTIFIER AS expression (NEWLINE|EOF)
    * (INDENT)* UNDEFINE IDENTIFIER (NEWLINE|EOF)
    * (INDENT)* DEFINE IDENTIFIER AS expression (NEWLINE|EOF)
    * (INDENT)* if_expression (NEWLINE|EOF)
    * (INDENT)* expression (NEWLINE|EOF)
- block
    * (line)*
