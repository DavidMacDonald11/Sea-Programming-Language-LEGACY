from .token import Token
from .token_types import TT
from .base_token_types import BaseTT
from .base_token_types import MAKE_MAP
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
                raise errors.UnknownTokenError(self.take_symbol())

    def construct_token(self):
        if not self.at_line_start and self.base_type is BaseTT.SPACE:
            self.take_symbol()
            return None

        if self.at_line_start and self.base_type is not BaseTT.SPACE:
            self.at_line_start = False

        position = self.position.copy()
        token = self.make_token()
        position.end = self.position.start.copy()
        token.position = position

        if self.base_type is BaseTT.NEWLINE:
            self.at_line_start = True
            self.position.start.next_line()

        self.advance()
        return token

    def take_symbol(self):
        self.took_symbol = True
        symbol = self.symbol

        self.advance()
        return symbol

    def advance(self):
        if self.took_symbol:
            self.symbol = self.input_stream.read() or None
            self.position.start.next()
            self.took_symbol = False

    def make_token(self):
        get_value = MAKE_MAP.get_value(self.base_type)
        other_valid_symbols = MAKE_MAP.other_valid_symbols(self.base_type)
        stop_if = MAKE_MAP.stop_if(self.base_type)

        token_string = ""

        if stop_if is None:
            stop_if = lambda x: False

        while self.symbol_is_valid(other_valid_symbols):
            token_string += self.take_symbol()

            if stop_if(token_string):
                break

        value = None if get_value is None else get_value(token_string)
        return Token(Token.match_type(token_string), value)

    def symbol_is_valid(self, other_valid_symbols = None):
        valid_symbols = self.base_type.value

        if other_valid_symbols is not None:
            valid_symbols = (*valid_symbols, *other_valid_symbols)

        return self.symbol is not None and self.symbol in valid_symbols
