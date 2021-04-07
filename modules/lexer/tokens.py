import re
import string
from enum import Enum
from enum import unique
from modules.helpers.repr_namespace import ReprNamespace
from .position import Position
from .keywords import is_keyword
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
    LPAREN = "("
    RPAREN = ")"

def match_type(token_string):
    for token_type in TT:
        if token_type.value.fullmatch(token_string) is not None:
            if token_type not in (TT.KEYWORD, TT.IDENTIFIER):
                return token_type

            return TT.KEYWORD if is_keyword(token_string) else TT.IDENTIFIER

    raise errors.UnknownTokenError(token_string)

def new_token(token_type, value = None, position = None):
    token = ReprNamespace()

    token.type = token_type
    token.value = value
    token.position = Position() if position is None else position

    def token_repr():
        return f"{token.type}" + ("" if token.value is None else f":{token.value}")

    token.repr = token_repr

    return token
