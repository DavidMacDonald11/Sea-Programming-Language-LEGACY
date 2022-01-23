from enum import Enum, unique
from lexing import errors
from .punctuator import Punctuator

class Operator(Punctuator):
    def __repr__(self):
        return f"Operator: {self.punctuator.value}"

    @classmethod
    def construct(cls, lexer):
        try:
            token_string = lexer.take_token_string(cls.symbols(), 2)
            operator = Op(token_string)
            return Operator(operator)
        except ValueError as e:
            raise errors.UnknownOperatorError(token_string) from e

    @classmethod
    def symbols(cls):
        return {operator.value for operator in Op}

@unique
class Op(Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    POWER = "**"
    DIVIDE = "/"
    MODULO = "%"
