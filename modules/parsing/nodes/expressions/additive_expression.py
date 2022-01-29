from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class AdditiveExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.multiplicative_expression,
                (Op.PLUS, Op.MINUS),
                parser.make.multiplicative_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
