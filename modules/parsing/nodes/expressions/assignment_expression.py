from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

ASSIGNMENT_OPERATORS = {
    Op.EQUALS,
    Op.PLUS_EQUALS,
    Op.MINUS_EQUALS,
    Op.MULTIPLY_EQUALS,
    Op.POWER_EQUALS,
    Op.DIVIDE_EQUALS,
    Op.MODULO_EQUALS,
    Op.LSHIFT_EQUALS,
    Op.RSHIFT_EQUALS,
    Op.AND_EQUALS,
    Op.XOR_EQUALS,
    Op.OR_EQUALS
}

class AssignmentExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.conditional_expression,
                ASSIGNMENT_OPERATORS,
                parser.make.assignment_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
