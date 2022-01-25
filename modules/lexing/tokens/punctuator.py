from enum import Enum, unique
from .token import Token

class Punctuator(Token):
    @property
    def data(self):
        return self.punctuator

    def __repr__(self):
        printable = value = self.punctuator.value

        if value == "":
            printable = "EOF"
        elif value == "\t":
            printable = "\\t"
        elif value == "\n":
            printable = "\\n"

        return f"P{{{printable}}}"

    def __init__(self, punctuator, position = None):
        self.punctuator = punctuator
        super().__init__(position)

    @classmethod
    def construct(cls, lexer):
        symbol = Punc(lexer.take())

        if symbol is Punc.NEWLINE:
            while lexer.symbol == "\n":
                lexer.position.end.advance_line()
                lexer.skip()

            lexer.position.end.advance_line()
            lexer.at_line_start = True

        return Punctuator(symbol)

    @classmethod
    def symbols(cls):
        return {punctuator.value for punctuator in Punc}

@unique
class Punc(Enum):
    INDENT = "\t"
    NEWLINE = "\n"
    LPAREN = "("
    RPAREN = ")"
    LBRACK = "["
    RBRACK = "]"
    COLON = ":"
    SEMICOLON = ";"
    COMMA = ","
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'
    EOF = ""
