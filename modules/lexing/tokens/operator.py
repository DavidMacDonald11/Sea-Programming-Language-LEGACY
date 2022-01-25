from enum import Enum, unique
from lexing import errors
from .punctuator import Punctuator

class Operator(Punctuator):
    @property
    def operator(self):
        return self.punctuator

    def __repr__(self):
        return f"O{{{self.operator.value}}}"

    @classmethod
    def construct(cls, lexer):
        try:
            token_string = lexer.take(cls.symbols(), 3)
            operator = Op(token_string)
            return Operator(operator)
        except ValueError as e:
            raise errors.UnknownOperatorError(token_string) from e

    @classmethod
    def symbols(cls):
        return {operator.value for operator in Op}

    def matches(self, what, *datas):
        return False if what is Punctuator else super().matches(what, *datas)

@unique
class Op(Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    POWER = "**"
    DIVIDE = "/"
    MODULO = "%"
    NOT = "~"
    LSHIFT = "<<"
    RSHIFT = ">>"
    AND = "&"
    XOR = "^"
    OR = "|"

    EQUALS = "="
    PLUS_EQUALS = "+="
    INCREMENT = "++"
    MINUS_EQUALS = "-="
    DECREMENT = "--"
    MULTIPLY_EQUALS = "*="
    POWER_EQUALS = "**="
    DIVIDE_EQUALS = "/="
    MODULO_EQUALS = "%="
    LSHIFT_EQUALS = "<<="
    RSHIFT_EQUALS = ">>="
    AND_EQUALS = "&="
    XOR_EQUALS = "^="
    OR_EQUALS = "|="

    EQ = "=="
    NE = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="

    ACCESS = "."
    POINTER_ACCESS = "->"
