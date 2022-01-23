from enum import Enum, unique
from .token import Token

class Punctuator(Token):
    @property
    def data(self):
        return self.punctuator

    def __repr__(self):
        return f"P{{{self.punctuator.value or 'EOF'}}}"

    def __init__(self, punctuator, position = None):
        self.punctuator = punctuator
        super().__init__(position)

    @classmethod
    def construct(cls, lexer):
        return Punctuator(Punc(lexer.take()))

    @classmethod
    def symbols(cls):
        return {punctuator.value for punctuator in Punc}

@unique
class Punc(Enum):
    INDENT = "\t"
    NEWLINE = "\n"
    LPAREN = "("
    RPAREN = ")"
    COLON = ":"
    SEMICOLON = ";"
    EOF = ""
