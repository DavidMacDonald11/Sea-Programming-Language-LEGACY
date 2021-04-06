from enum import Enum
from types import SimpleNamespace
from .position import Position

class TT(Enum):
    INDENT = " \t"
    NEWLINE = "\n"
    INT = "0123456789"
    FLOAT = INT + "."
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    LPAREN = "("
    RPAREN = ")"
    EOF = ""

def new_token(token_type, value = None, position = None):
    token = SimpleNamespace()

    token.type = token_type
    token.value = value
    token.position = Position() if position is None else position

    def token_repr():
        return f"{token.type}" + ("" if token.value is None else f":{token.value}")

    token.__repr__ = token_repr

    return token
