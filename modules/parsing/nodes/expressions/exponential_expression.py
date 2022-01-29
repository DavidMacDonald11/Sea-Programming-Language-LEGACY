from lexing.tokens.operator import Op
from .binary_expression import BinaryExpressionNode

class ExponentialExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.postfix_expression,
                (Op.POWER,),
                parser.make.cast_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
