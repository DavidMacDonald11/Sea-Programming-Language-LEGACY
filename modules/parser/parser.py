from modules.lexer.tokens import TT
from ..parser import nodes
from ..parser import errors

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_i = -1
        self.token = None
        self.advance()

    def take_token(self):
        token = self.token
        self.advance()
        return token

    def advance(self):
        self.token_i += 1

        if self.token_i < len(self.tokens):
            self.token = self.tokens[self.token_i]

        return self.token

    def parse(self):
        return self.expression()

    def atom(self):
        if self.token.type in (TT.INT, TT.FLOAT):
            return nodes.new_number_node(self.take_token())

        if self.token.type == TT.IDENTIFIER:
            return nodes.new_var_access_node(self.take_token())

        if self.token.type == TT.LPAREN:
            self.advance()
            node = self.expression()

            if self.token.type == TT.RPAREN:
                self.advance()
                return node

            raise errors.NoClosingParenthesisError(self.token)

        raise errors.AtomError(self.token)

    def power(self):
        return self.binary_operation(self.atom, (TT.POWER,), self.factor)

    def factor(self):
        if self.token.type in (TT.PLUS, TT.MINUS):
            operation_token = self.take_token()
            return nodes.new_unary_operation_node(operation_token, self.factor())

        return self.power()

    def term(self):
        return self.binary_operation(self.factor, (TT.MULTIPLY, TT.DIVIDE))

    def arithmetic_expression(self):
        return self.binary_operation(self.term, (TT.PLUS, TT.MINUS))

    def comparison_expression(self):
        if self.token.matches(TT.KEYWORD, "not"):
            operation_token = self.take_token()
            node = self.comparison_expression()

            return nodes.new_unary_operation_node(operation_token, node)

        operations = (TT.EQ, TT.NE, TT.LT, TT.GT, TT.LTE, TT.GTE)

        return self.binary_operation(self.arithmetic_expression, operations)

    def expression(self):
        if not self.token.matches_type_keyword():
            operations = ((TT.KEYWORD, "and"), (TT.KEYWORD, "or"))
            return self.binary_operation(self.comparison_expression, operations)

        keyword_token = self.take_token()

        if self.token.type is not TT.IDENTIFIER:
            raise errors.NoIdentifierError(self.token)

        variable_token = self.take_token()

        if self.token.type is not TT.EQUALS:
            raise errors.NoEqualsError(self.token)

        self.advance()

        return nodes.new_var_assign_node(keyword_token, variable_token, self.expression())

    def binary_operation(self, left_func, operations, right_func = None):
        if right_func is None:
            right_func = left_func

        left = left_func()
        token_type_value = (self.token.type, self.token.value)

        while self.token.type in operations or token_type_value in operations:
            operation_token = self.take_token()
            right = right_func()
            left = nodes.new_binary_operation_node(left, operation_token, right)

            token_type_value = (self.token.type, self.token.value)

        return left
