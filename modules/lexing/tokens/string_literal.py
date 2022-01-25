from lexing import errors
from .constant import Constant

class StringLiteral(Constant):
    @classmethod
    @property
    def label(cls):
        return "S"

    @classmethod
    def construct(cls, lexer):
        satisfied = lambda x: len(x) > 1 and x[-1] == x[0] and x[-2] != "\\"
        token_string = lexer.take(True, until = satisfied)

        if not satisfied(token_string):
            raise errors.UnterminatedStringError()

        return StringLiteral(token_string)

    @classmethod
    def symbols(cls):
        return "'\""
