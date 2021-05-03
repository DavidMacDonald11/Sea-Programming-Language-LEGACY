from enum import Enum, unique
from .token import Token

class Symbol(Token):
    @property
    def data(self):
        return self.symbol

    def __init__(self, symbol, position = None):
        self.symbol = symbol
        super().__init__(position)

    @classmethod
    def construct(cls, lexer):
        symbol = Sym(lexer.take())

        if symbol is Sym.NEWLINE:
            while lexer.symbol == "\n":
                lexer.position.end.advance_line()
                lexer.skip()

            lexer.position.end.advance_line()
            lexer.at_line_start = True

        return Symbol(symbol)

    @classmethod
    def allowed(cls):
        return {symbol.value for symbol in Sym}

@unique
class Sym(Enum):
    INDENT = "\t"
    NEWLINE = "\n"
    LPAREN = "("
    RPAREN = ")"
    COLON = ":"
    SEMICOLON = ";"
    EOF = ""
