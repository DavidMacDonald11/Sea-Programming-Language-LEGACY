from . import errors
from .nodes.makes import MAKES, set_parser

class Parser:
    @property
    def tokens(self):
        return self.lexer.tokens

    @property
    def token(self):
        return self.tokens[min(self.i, len(self.tokens) - 1)]

    @property
    def make(self):
        return MAKES

    def __init__(self, lexer):
        self.lexer = lexer
        self.depth = 0
        self.i = 0
        self.ast = None

        set_parser(self)

    def advance(self, amount = 1):
        if amount < 1:
            return

        self.i += amount

    def take(self, amount = 1):
        if amount < 1:
            return None

        i = self.i
        self.advance(amount)

        return self.tokens[i:self.i] or [self.tokens[-1]]

    def untake(self, amount = 1):
        if amount < 1:
            return

        self.i = max(self.i - amount, 0)

    def expecting(self, *datas, check_type = False):
        for data in datas:
            if check_type:
                condition = isinstance(self.token, data)
            else:
                data_tuple = data if isinstance(data, (tuple, list)) else (data,)
                condition = self.token.data in data_tuple

            if not condition:
                raise errors.ExpectedTokenError(data)

            self.advance()

        self.untake(len(datas))
        return self.take(len(datas))

    def wanting(self, *datas):
        try:
            i = self.i
            return self.expecting(*datas)
        except errors.ExpectedTokenError:
            self.i = i
            return None

    def make_nodes(self):
        self.ast = self.make.primary_expression()
