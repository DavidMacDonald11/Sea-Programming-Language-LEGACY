from enum import Enum
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

class Token:
    def __init__(self, token_type, value = None, position = None):
        self.type = token_type
        self.value = value
        self.position = Position() if position is None else position

    def __repr__(self):
        return f"{self.type}" + ("" if self.value is None else f":{self.value}")
