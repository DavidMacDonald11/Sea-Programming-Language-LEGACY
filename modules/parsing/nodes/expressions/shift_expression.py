from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class ShiftExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.additive_expression,
                (Op.LSHIFT, Op.RSHIFT),
                parser.make.additive_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
