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
    EQUALS = "="
    PAREN = "()"
    CHEVRON = "<>"
    EXCLAMATION = "!"
    COLON = ":"

GET_VALUE = {
    BaseTT.IDENTIFIER: (lambda x: x),
    BaseTT.NUMBER: (lambda x: x)
}

OTHER_VALID_SYMBOLS = {
    BaseTT.EXCLAMATION: "=",
    BaseTT.CHEVRON: "="
}

SIZE_OF_ONE = lambda x: len(x) == 1

STOP_IF = {
    BaseTT.SPACE: (lambda x: "\t" in x or " " * 4 in x),
    BaseTT.NEWLINE: SIZE_OF_ONE,
    BaseTT.PLUS: SIZE_OF_ONE,
    BaseTT.MINUS: SIZE_OF_ONE,
    BaseTT.SLASH: SIZE_OF_ONE,
    BaseTT.PAREN: SIZE_OF_ONE,
    BaseTT.COLON: SIZE_OF_ONE

}

MAKE_MAP = SimpleNamespace(
    get_value = GET_VALUE.get,
    other_valid_symbols = OTHER_VALID_SYMBOLS.get,
    stop_if = STOP_IF.get
)
