from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class BitwiseXorExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.bitwise_and_expression,
                (Op.XOR,),
                parser.make.bitwise_and_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
