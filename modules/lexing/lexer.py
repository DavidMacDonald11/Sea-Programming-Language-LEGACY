from . import errors
from .position.position import Position
from .position.symbol_position import SymbolPosition
from .tokens.punctuator import Punctuator
from .tokens.operator import Operator
from .tokens.constant import NumericalConstant
from .tokens.keyword import Keyword

class Lexer:
    def __init__(self, in_stream):
        self.in_stream = in_stream
        self.position = Position(in_stream, SymbolPosition(1, 1), SymbolPosition(1, 0))
        self.at_line_start = True
        self.symbol = ""
        self.tokens = []

        self.skip()

    def skip(self):
        self.symbol = self.in_stream.read_symbol()

    def advance(self):
        self.skip()
        self.position.end.advance()

    def take(self, symbols = None, max_len = None):
        if symbols is None:
            symbol = self.symbol
            self.advance()

            return symbol

        token_string = ""

        while self.symbol in symbols:
            token_string += self.take()

            if max_len is not None and len(token_string) == max_len:
                break

        return token_string

    def new_position(self):
        self.position = Position(self.in_stream, self.position.end.copy())
        self.position.start.advance()

        return self.position

    def make_tokens(self):
        while self.symbol != "":
            self.tokens += [self.take_token()]

    def take_token(self):
        while self.symbol.isspace():
            self.advance()

        position = self.new_position()

        for token_type in (Punctuator, Operator, NumericalConstant, Keyword):
            if self.symbol in token_type.symbols():
                token = token_type.construct(self)
                token.position = position

                return token

        raise errors.UnknownSymbolError(self.take())
