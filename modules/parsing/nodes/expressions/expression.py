from lexing.tokens.punctuator import Punc
from .binary_expression import BinaryExpressionNode

class ExpressionNode(BinaryExpressionNode):
    @classmethod
    def construct_info(cls, parser):
        return (parser.make.assignment_expression,
                (Punc.COMMA,),
                parser.make.assignment_expression)

    def interpret(self):
        pass

    def transpile(self):
        pass
