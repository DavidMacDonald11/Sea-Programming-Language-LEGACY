from enum import Enum, unique
from lexer import errors
from .token import Token

class Operator(Token):
    @property
    def data(self):
        return self.operator

    def __init__(self, operator, position = None):
        self.operator = operator
        super().__init__(position)

    def __repr__(self):
        return f"Operator: {self.operator.value}"

    @classmethod
    def construct(cls, lexer):
        token_string = lexer.take_token_string(cls.allowed())
        operator = cls.get_operator(token_string)

        return Operator(operator)

    @classmethod
    def get_operator(cls, token_string):
        try:
            return Op(token_string)
        except KeyError as e:
            raise errors.UnknownOperatorError(token_string) from e

    @classmethod
    def allowed(cls):
        return {c for op in Op for c in op.value}

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
