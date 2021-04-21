import re
from enum import Enum
from enum import unique
from ..lexer import errors

@unique
class TT(Enum):
    INDENT = re.compile(r" {4}|\t")
    NEWLINE = re.compile(r"\n")
    IDENTIFIER = re.compile(r"[a-zA-Z_]+\w*")
    KEYWORD = re.compile(r"[a-zA-Z_]+\w+")
    INT = re.compile(r"[0-9]+")
    FLOAT = re.compile(r"[0-9]*\.+[0-9]+")
    LPAREN = re.compile(r"\(")
    RPAREN = re.compile(r"\)")
    PLUS = re.compile(r"\+")
    MINUS = re.compile(r"\-")
    MULTIPLY = re.compile(r"\*")
    POWER = re.compile(r"\*{2}")
    DIVIDE = re.compile(r"\/")
    MODULO = re.compile(r"\%")
    EQUALS = re.compile(r"\=")
    NE = re.compile(r"\!\=")
    EQ = re.compile(r"\={2}")
    LT = re.compile(r"\<")
    GT = re.compile(r"\>")
    LTE = re.compile(r"\<\=")
    GTE = re.compile(r"\>\=")
    COLON = re.compile(r"\:")
    SEMICOLON = re.compile(r"\;")
    NOT = re.compile(r"\~")
    LSHIFT = re.compile(r"\<\<")
    RSHIFT = re.compile(r"\>\>")
    AND = re.compile(r"\&")
    XOR = re.compile(r"\^")
    OR = re.compile(r"\|")
    EOF = re.compile("")

@unique
class BadTT(Enum):
    FLOAT = (re.compile(r"[0-9.]+"), errors.FloatError)
    INDENT = (re.compile(r"\s+"), errors.IndentError)
