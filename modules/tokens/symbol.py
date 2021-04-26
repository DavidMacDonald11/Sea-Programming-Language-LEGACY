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
        pass

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
