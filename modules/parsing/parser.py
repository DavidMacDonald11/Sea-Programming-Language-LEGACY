from . import errors
from .nodes.makes import MAKES, set_parser

class Parser:
    @property
    def tokens(self):
        return self.lexer.tokens

    @property
    def token(self):
        return self.tokens[self.i]

    @property
    def make(self):
        return MAKES

    def __init__(self, lexer):
        self.lexer = lexer
        self.depth = 0
        self.i = 0
        self.ast = None

        set_parser(self)

    def advance(self):
        if self.i < len(self.tokens) - 1:
            self.i += 1

    def take(self):
        token = self.token
        self.advance()

        return token

    def untake(self, amount = 1):
        if amount < 1:
            return

        self.i = max(self.i - amount, 0)

    def expecting(self, *datas, what = None):
        if not self.token.matches(what or type(self.token), *datas):
            raise errors.ExpectedTokenError(what, *datas)

        return self.take()

    def wanting(self, *datas, what = None):
        try:
            return self.expecting(*datas, what = what)
        except errors.ExpectedTokenError:
            return None

    def make_nodes(self):
        self.ast = self.make.cast_expression()
