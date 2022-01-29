from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class MultiplicativeExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.cast_expression,
                (Op.MULTIPLY, Op.DIVIDE, Op.MODULO),
                parser.make.cast_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
