from functools import cached_property
from .tokens import TT
from .tokens import Token
from .position import Position
from .position import FilePosition
from ..lexer import errors

class Lexer:
    @cached_property
    def make_map(self):
        return {
            TT.INDENT: self.make_indent,
            TT.INT: self.make_number,
            TT.FLOAT: self.make_number
        }

    def __init__(self, file):
        self.file = file
        self.position = Position(FilePosition(file))

        self.at_line_start = True
        self.token_type = None
        self.symbol = None
        self.took_symbol = True

        self.advance()

    def make_tokens(self):
        return list(self.generate_tokens()) + [Token(TT.EOF)]

    def generate_tokens(self):
        while self.symbol is not None:
            for token_type in TT:
                if self.symbol in token_type.value:
                    self.token_type = token_type

                    new_token = self.make_token()

                    if new_token is not None:
                        yield new_token

                    break
            else:
                raise errors.UnknownTokenError(self.take_symbol_and_advance())

    def make_token(self):
        position = self.position.copy()

        if self.at_line_start and self.token_type is not TT.INDENT:
            self.at_line_start = False
        elif not self.at_line_start and self.token_type is TT.INDENT:
            self.take_symbol_and_advance()
            return None

        position.end = self.position.copy().start
        new_token = self.make()
        new_token.position = position

        if self.token_type is TT.NEWLINE:
            self.at_line_start = True
            self.position.start.next_line()
            self.take_symbol_and_advance()

        self.advance()
        return new_token

    def take_symbol_and_advance(self):
        symbol = self.take_symbol()
        self.advance()
        return symbol

    def advance(self):
        if self.took_symbol:
            self.symbol = self.file.read(1) or None
            self.position.start.next()
            self.took_symbol = False

    def take_symbol(self):
        self.took_symbol = True
        return self.symbol

    def make(self):
        try:
            return self.make_map[self.token_type]()
        except KeyError:
            self.take_symbol_and_advance()
            return Token(self.token_type)

    def make_indent(self):
        indent_str = ""

        while self.symbol_is_valid():
            indent_str += self.take_symbol()

            if "\t" in indent_str or " " * 4 in indent_str:
                return Token(TT.INDENT)

            self.advance()

        raise errors.IndentError()

    def make_number(self):
        num_str = ""
        dot_count = 0

        while self.symbol_is_valid():
            num_str += self.take_symbol_and_advance()

            if self.symbol == ".":
                dot_count += 1

                if dot_count == 2:
                    raise errors.FloatError()

        return Token(TT.INT if dot_count == 0 else TT.FLOAT, num_str)

    def symbol_is_valid(self):
        return self.symbol is not None and self.symbol in self.token_type.value
