from position.position import Position
from position.char_position import CharPosition
from tokens.symbol import Symbol, Sym
from tokens.keyword import Keyword
from tokens.literal import Literal
from tokens.operator import Operator
from lexer import errors

class Lexer:
    def __init__(self, in_stream):
        self.in_stream = in_stream
        self.position = Position(in_stream, CharPosition(1, 1), CharPosition(1, 0))
        self.at_line_start = True
        self.symbol = ""
        self.tokens = []

        self.skip()

    def skip(self):
        self.symbol = self.in_stream.read(1)

    def advance(self):
        self.skip()
        self.position.end.advance()

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

    def take_position(self):
        self.position = Position(self.in_stream, self.position.end.copy())
        self.position.start.advance()

        return self.position

    def make_tokens(self):
        while self.symbol != "":
            self.tokens += [self.construct_token()]

        self.tokens += [Symbol(Sym.EOF, self.position.copy())]

    def check_spaces(self):
        is_space = self.symbol == " "
        is_tab = self.symbol == "\t"
        is_indent = is_space or is_tab

        if not self.at_line_start:
            if is_indent:
                self.advance()

            return False

        if not is_indent:
            self.at_line_start = False
            return False

        if is_space:
            token_string = self.take_token_string(" ", 4)

            if token_string != " " * 4:
                raise errors.IndentError()

            return True

        return False

    def construct_token(self):
        position = self.take_position()

        if self.check_spaces():
            token = Symbol(Sym.INDENT)
            token.position = position

            return token

        position = self.take_position()

        for token_type in (Symbol, Literal, Operator, Keyword):
            if self.symbol in token_type.allowed():
                token = token_type.construct(self)
                token.position = position

                return token

        raise errors.UnknownSymbolError(self.symbol)
