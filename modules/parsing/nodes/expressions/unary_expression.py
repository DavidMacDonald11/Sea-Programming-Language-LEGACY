from types import SimpleNamespace
from lexing.tokens.operator import Op
from ..node import Node

UNARY_OPERATORS = (
    Op.PLUS,
    Op.MINUS,
    Op.NOT,
    Op.AND,
    Op.MULTIPLY
)

# TODO add not keyword with correct priority
# TODO Implment align of?

class UnaryExpressionNode(Node):
    @classmethod
    def construct(cls, parser):
        if parser.token.matches_data(Op.INCREMENT, Op.DECREMENT):
            return UnaryExpressionNode(parser.take(), parser.make.unary_expression())

        if parser.token.matches_data(*UNARY_OPERATORS):
            return UnaryExpressionNode(parser.take(), parser.make.cast_expression())

        if parser.token.matches_data("size"):
            return UnaryExpressionNode(
                parser.take(),
                parser.expecting("of"),
                parser.make.unary_expression()
                )

        return parser.make.postfix_expression()

    def interpret(self):
        pass

    def transpile(self):
        pass
