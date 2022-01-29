from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class ComparisonExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.bitwise_or_expression,
                (Op.LT, Op.GT, Op.LTE, Op.GTE, Op.EQ, Op.NE),
                parser.make.bitwise_or_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
