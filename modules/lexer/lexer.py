from functools import cached_property
from .tokens import Token
from .position import Position, FilePosition
from ..lexer import errors

class Lexer:
    @cached_property
    def make_map(self):
        return {
            "INDENT": self.make_indent,
            "INT": self.make_number,
            "FLOAT": self.make_number
        }

    def __init__(self, file):
        self.file = file
        self.file_position = FilePosition(file)
        self.end_position = None

        self.symbol = None
        self.took_symbol = True

        self.advance()

    def take_symbol_and_advance(self):
        symbol = self.take_symbol()
        self.advance()
        return symbol

    def advance(self):
        if self.took_symbol:
            self.symbol = self.file.read(1) or None
            self.file_position.next()
            self.took_symbol = False

    def take_symbol(self):
        self.took_symbol = True
        return self.symbol

    def make_tokens(self):
        at_line_start = True
        tokens = []

        while self.symbol is not None:
            position = Position(self.file_position.copy())
            matched_token = False

            for symbols, token_type in Token.TYPES.items():
                if self.symbol in symbols:
                    matched_token = True

                    if at_line_start and token_type != "INDENT":
                        at_line_start = False
                    elif not at_line_start and token_type == "INDENT":
                        self.take_symbol_and_advance()
                        continue

                    position.end = self.file_position.copy()
                    new_token = self.make(token_type)
                    new_token.position = position

                    tokens += [new_token]

                    if token_type == "LINEEND":
                        at_line_start = True
                        self.file_position.next_line()
                        self.take_symbol_and_advance()

                    self.advance()
                    break

            if not matched_token:
                raise errors.UnknownTokenError(self.take_symbol_and_advance())

        return tokens + [Token("EOF")]

    def make(self, token_type):
        try:
            return self.make_map[token_type]()
        except KeyError:
            self.take_symbol_and_advance()
            return Token(token_type)

    def make_indent(self):
        indent_str = ""

        while self.symbol is not None and self.symbol in Token.SYMBOLS["INDENT"]:
            indent_str += self.take_symbol()

            if "\t" in indent_str or " " * 4 in indent_str:
                return Token("INDENT")

            self.advance()

        raise errors.IndentError()

    def make_number(self):
        num_str = ""
        dot_count = 0

        while self.symbol is not None and self.symbol in Token.SYMBOLS["FLOAT"]:
            if self.symbol == ".":
                if dot_count == 1:
                    self.take_symbol_and_advance()
                    raise errors.FloatError()

                dot_count += 1

            num_str += self.take_symbol_and_advance()

        return Token("INT" if dot_count == 0 else "FLOAT", num_str)