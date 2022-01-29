from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class BitwiseOrExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.bitwise_xor_expression,
                (Op.OR,),
                parser.make.bitwise_xor_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
