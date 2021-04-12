from .tokens import TT
from .tokens import BaseTT
from .tokens import match_type
from .tokens import Token
from .position import Position
from .position import FilePosition
from ..lexer import errors

class Lexer:
    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.position = Position(FilePosition(input_stream))

        self.at_line_start = True
        self.base_type = None
        self.symbol = None
        self.took_symbol = True

        self.advance()

    def make_tokens(self):
        return list(self.generate_tokens()) + [Token(TT.EOF)]

    def generate_tokens(self):
        while self.symbol is not None:
            for base_type in BaseTT:
                if self.symbol in base_type.value:
                    self.base_type = base_type

                    token = self.construct_token()

                    if token is not None:
                        yield token

                    break
            else:
                raise errors.UnknownTokenError(self.take_symbol_and_advance())

    def construct_token(self):
        if self.at_line_start and self.base_type is not BaseTT.SPACE:
            self.at_line_start = False
        elif not self.at_line_start and self.base_type is BaseTT.SPACE:
            self.take_symbol_and_advance()
            return None

        position = self.position.copy()
        token = self.make_token()
        position.end = self.position.start.copy()
        token.position = position

        if self.base_type is BaseTT.NEWLINE:
            self.at_line_start = True
            self.position.start.next_line()

        self.advance()
        return token

    def take_symbol_and_advance(self):
        symbol = self.take_symbol()
        self.advance()
        return symbol

    def take_symbol(self):
        self.took_symbol = True
        return self.symbol

    def advance(self):
        if self.took_symbol:
            self.symbol = self.input_stream.read() or None
            self.position.start.next()
            self.took_symbol = False

    def symbol_is_valid(self, also_valid = None):
        valid = self.base_type.value

        if also_valid is not None:
            valid = (*valid, *also_valid)

        return self.symbol is not None and self.symbol in valid

    def make_token(self):
        get_value = make_map_get_value.get(self.base_type, None)
        also_valid = make_map_also_valid.get(self.base_type, None)
        stop_if = make_map_stop_if.get(self.base_type, None)

        string = ""

        if stop_if is None:
            stop_if = lambda x: False

        while self.symbol_is_valid(also_valid):
            string += self.take_symbol_and_advance()

            if stop_if(string):
                break

        value = None if get_value is None else get_value(string)
        return Token(match_type(string), value)

make_map_get_value = {
    BaseTT.IDENTIFIER: (lambda x: x),
    BaseTT.NUMBER: (lambda x: x)
}

make_map_also_valid = {
    BaseTT.EXCLAMATION: "=",
    BaseTT.CHEVRON: "="
}

size_of_one = lambda x: len(x) == 1

make_map_stop_if = {
    BaseTT.SPACE: (lambda x: "\t" in x or " " * 4 in x),
    BaseTT.NEWLINE: size_of_one,
    BaseTT.PLUS: size_of_one,
    BaseTT.MINUS: size_of_one,
    BaseTT.SLASH: size_of_one,
    BaseTT.PAREN: size_of_one,
    BaseTT.COLON: size_of_one
}
