from position.position import Position
from tokens.symbol import Symbol, Sym
from tokens.literal import Literal
from tokens.operator import Operator
from tokens.identifier import Identifier
from lexer import errors

class Lexer:
    def __init__(self, in_stream):
        self.in_stream = in_stream
        self.position = Position(in_stream)
        self.at_line_start = True
        self.symbol = ""

        self.advance()

    def advance(self):
        self.symbol = self.in_stream.read(1)

    def take(self):
        symbol = self.symbol
        self.advance()

        return symbol

    def take_token_string(self, allowed, max_length = None):
        token_string = ""

        while self.symbol in allowed:
            token_string += self.take()

            if max_length is not None and len(token_string) == max_length:
                break

        return token_string

    def make_tokens(self):
        return list(self.generate_tokens())

    def generate_tokens(self):
        while self.symbol != "":
            self.check_spaces()

            position = self.position.copy()
            token = self.construct_token()
            position.end = self.position.start.copy()
            token.position = position

            yield token

        return Symbol(Sym.EOF, self.position.copy())

    def check_spaces(self):
        is_space = self.symbol == " "
        is_tab = self.symbol == "\t"
        is_indent = is_space or is_tab

        if not self.at_line_start:
            if is_indent:
                self.take()

            return

        if not is_indent:
            self.at_line_start = False
            return

        if is_space:
            token_string = self.take_token_string(" ", 4)

            if token_string != " " * 4:
                raise errors.IndentError()

            self.symbol = "\t"

    def construct_token(self):
        for token_type in {Symbol, Operator, Literal, Identifier}:
            if self.symbol in token_type.allowed():
                return token_type.construct(self)

        raise errors.UnknownSymbolError(self.symbol)
