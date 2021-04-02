from .ast.nodes import NumberNode
from .ast.nodes import BinaryOperationNode
from .ast.nodes import UnaryOperationNode
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

    def factor(self):
        if self.token.type in ("PLUS", "MINUS"):
            operation_token = self.take_token()
            return UnaryOperationNode(operation_token, self.factor())
        elif self.token.type in ("INT", "FLOAT"):
            return NumberNode(self.take_token())
        elif self.token.type == "LPAREN":
            self.advance()
            node = self.expression()

            if self.token.type == "RPAREN":
                self.advance()
                return node

            raise errors.NoClosingParenthesisError(self.token)

        raise errors.FactorError(self.token)

    def term(self):
        return self.binary_operation(self.factor, ("MUL", "DIV"))

    def expression(self):
        return self.binary_operation(self.term, ("PLUS", "MINUS"))

    def binary_operation(self, func, operations):
        left = func()

        while self.token.type in operations:
            operation_token = self.take_token()
            right = func()
            left = BinaryOperationNode(left, operation_token, right)

        return left
