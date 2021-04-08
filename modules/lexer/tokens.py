import re
import string
from enum import Enum
from enum import unique
from .position import Position
from .keywords import is_keyword
from .keywords import keyword_declared_type
from ..lexer import errors

@unique
class TT(Enum):
    INDENT = re.compile(r" {4}|\t")
    NEWLINE = re.compile(r"\n")
    IDENTIFIER = re.compile(r"[a-zA-Z_]+\w*")
    KEYWORD = re.compile(r"[a-zA-Z_]+\w+")
    INT = re.compile(r"[0-9]+")
    FLOAT = re.compile(r"[0-9]*\.+[0-9]+")
    PLUS = re.compile(r"\+")
    MINUS = re.compile(r"\-")
    MULTIPLY = re.compile(r"\*")
    POWER = re.compile(r"\*{2}")
    DIVIDE = re.compile(r"\/")
    EQUALS = re.compile(r"\=")
    NE = re.compile(r"\!\=")
    EQ = re.compile(r"\={2}")
    LT = re.compile(r"\<")
    GT = re.compile(r"\>")
    LTE = re.compile(r"\<\=")
    GTE = re.compile(r"\>\=")
    LPAREN = re.compile(r"\(")
    RPAREN = re.compile(r"\)")
    EOF = re.compile("")

@unique
class BaseTT(Enum):
    SPACE = " \t"
    NEWLINE = "\n"
    NUMBER = "0123456789."
    IDENTIFIER = string.ascii_letters + "0123456789_"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    EQUALS = "="
    PAREN = "()"
    CHEVRON = "<>"
    EXCLAMATION = "!"

@unique
class BadTT(Enum):
    FLOAT = (re.compile(r"[0-9.]+"), errors.FloatError)
    INDENT = (re.compile(r"\s+"), errors.IndentError)

def match_type(token_string):
    for token_type in TT:
        if token_type.value.fullmatch(token_string) is not None:
            if token_type not in (TT.KEYWORD, TT.IDENTIFIER):
                return token_type

            return TT.KEYWORD if is_keyword(token_string) else TT.IDENTIFIER

    for bad_type in BadTT:
        if bad_type.value[0].fullmatch(token_string) is not None:
            raise bad_type.value[1]()

    raise errors.UnknownTokenError(token_string)

class Token:
    def __init__(self, token_type, value = None, position = None):
        self.type = token_type
        self.value = value
        self.position = Position() if position is None else position

    def __repr__(self):
        return f"{self.type}" + ("" if self.value is None else f":{self.value}")

    def matches(self, token_type, value):
        return self.type is token_type and self.value == value

    def matches_type_keyword(self):
        return self.type is TT.KEYWORD and keyword_declared_type(self.value)
