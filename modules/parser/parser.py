from modules.lexer.tokens import TT
from modules.lexer.keywords import keyword_declared_type
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

    def expression(self):
        if self.token.type is not TT.KEYWORD or not keyword_declared_type(self.token.value):
            return self.binary_operation(self.term, (TT.PLUS, TT.MINUS))

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

        while self.token.type in operations:
            operation_token = self.take_token()
            right = right_func()
            left = nodes.new_binary_operation_node(left, operation_token, right)

        return left
