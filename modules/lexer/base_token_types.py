import string
from types import SimpleNamespace
from enum import Enum
from enum import unique

@unique
class BaseTT(Enum):
    NEWLINE = "\n"
    SPACE = " \t"
    NUMBER = "0123456789."
    IDENTIFIER = string.ascii_letters + "0123456789_"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    EQUALS = "="
    PAREN = "()"
    CHEVRON = "<>"
    EXCLAMATION = "!"
    COLON = ":"
    SEMICOLON = ";"
    TILDE = "~"
    AMPERSAND = "&"
    CARET = "^"
    PIPE = "|"

GET_VALUE = {
    BaseTT.IDENTIFIER: (lambda x: x),
    BaseTT.NUMBER: (lambda x: x)
}

OTHER_VALID_SYMBOLS = {
    BaseTT.EXCLAMATION: "=",
    BaseTT.CHEVRON: "=",
    BaseTT.PLUS: "=",
    BaseTT.MINUS: "=",
    BaseTT.STAR: "=",
    BaseTT.SLASH: "=",
    BaseTT.PERCENT: "=",
    BaseTT.TILDE: "=",
    BaseTT.AMPERSAND: "=",
    BaseTT.CARET: "=",
    BaseTT.PIPE: "="
}

def size_matches(size):
    def matches(x):
        return len(x) == size

    return matches

STOP_IF = {
    BaseTT.SPACE: (lambda x: "\t" in x or " " * 4 in x),
    BaseTT.NEWLINE: size_matches(1),
    BaseTT.PAREN: size_matches(1),
    BaseTT.COLON: size_matches(1),
    BaseTT.SEMICOLON: size_matches(1),
}

MAKE_MAP = SimpleNamespace(
    get_value = GET_VALUE.get,
    other_valid_symbols = OTHER_VALID_SYMBOLS.get,
    stop_if = STOP_IF.get
)
