from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class BitwiseAndExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.shift_expression,
                (Op.AND,),
                parser.make.shift_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
