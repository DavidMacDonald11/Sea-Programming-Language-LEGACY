from position.position import Position
from position.symbol_position import SymbolPosition
from . import errors

class Lexer:
    def __init__(self, in_stream):
        self.in_stream = in_stream
        self.position = Position(in_stream, SymbolPosition(1, 1), SymbolPosition(1, 0))
        self.at_line_start = True
        self.symbol = ""
        self.tokens = []

        self.skip()

    def skip(self):
        self.symbol = self.in_stream.read()

    def advance(self):
        self.skip()
        self.position.end.advance()

    def take(self):
        symbol = self.symbol
        self.advance()

        return symbol

    def take_token_string(self, symbols, max_length = None):
        token_string = ""

        while self.symbol in symbols:
            token_string += self.take()

            if max_length is not None and len(token_string) == max_length:
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
        return ""
