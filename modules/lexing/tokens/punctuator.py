from enum import Enum, unique
from .token import Token
from .. import errors

class Punctuator(Token):
    @property
    def data(self):
        return self.punctuator

    def __repr__(self):
        return f"Punctuator: {self.punctuator.value or 'EOF'}"

    def __init__(self, punctuator, position = None):
        self.punctuator = punctuator
        super().__init__(position)

    @classmethod
    def construct(cls, lexer):
        return Punctuator(Punc(lexer.take()))

    @classmethod
    def symbols(cls):
        return {punctuator.value for punctuator in Punc}

class Operator(Punctuator):
    def __repr__(self):
        return f"Operator: {self.punctuator.value}"

    @classmethod
    def construct(cls, lexer):
        try:
            token_string = lexer.take_token_string(cls.symbols(), 2)
            operator = Op(token_string)
            return Operator(operator)
        except ValueError:
            raise errors.UnknownOperatorError(token_string)

    @classmethod
    def symbols(cls):
        return {operator.value for operator in Op}

@unique
class Punc(Enum):
    LPAREN = "("
    RPAREN = ")"
    EOF = ""

@unique
class Op(Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    POWER = "**"
    DIVIDE = "/"
    MODULO = "%"
