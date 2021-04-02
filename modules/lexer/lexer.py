from functools import cached_property
from .tokens import Token
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
        self.position = -1
        self.line_count = 1
        self.column_count = -1

        self.symbol = None
        self.took_symbol = True

        self.advance()

    def take_symbol_and_advance(self):
        symbol = self.take_symbol()
        self.advance()
        return symbol

    def advance(self):
        if self.took_symbol:
            self.position += 1
            self.symbol = self.file.read(1) or None
            self.column_count += 1
            self.took_symbol = False

    def take_symbol(self):
        self.took_symbol = True
        return self.symbol

    def make_tokens(self):
        at_line_start = True
        tokens = []

        while self.symbol is not None:
            if self.symbol == "\n":
                at_line_start = True
                self.line_count += 1
                self.column_count = -1

                self.take_symbol_and_advance()
                continue

            matched_token = False

            for symbols, token_type in Token.TYPES.items():
                if self.symbol in symbols:
                    matched_token = True

                    if at_line_start and token_type != "INDENT":
                        at_line_start = False
                    elif not at_line_start and token_type == "INDENT":
                        self.take_symbol_and_advance()
                        continue

                    tokens += [self.make(token_type)]

                    self.advance()
                    break

            if not matched_token:
                raise errors.UnknownTokenError(self.take_symbol_and_advance())

        return tokens

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
                    raise errors.FloatError()

                dot_count += 1

            num_str += self.take_symbol_and_advance()

        return Token("INT", int(num_str)) if dot_count == 0 else Token("FLOAT", float(num_str))
