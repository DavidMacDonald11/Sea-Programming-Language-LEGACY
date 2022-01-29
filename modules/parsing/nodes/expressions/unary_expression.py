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

# TODO Implment align of?

class UnaryExpressionNode(Node):
    @property
    def operator(self):
        return self.components[0]

    @property
    def expression(self):
        return self.components[-1]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        operator = f"{spacing}{down}{self.operator if self.operator != 'size' else 'size of'}"
        expression = f"{spacing}{bottom}{self.expression.tree_repr(depth + 1)}"

        return f"{self.node_name}{operator}{expression}"

    @classmethod
    def construct(cls, parser):
        if parser.token.matches_data(*UNARY_OPERATORS):
            return UnaryExpressionNode(parser.take(), parser.make.cast_expression())

        if parser.token.matches_data("size"):
            return UnaryExpressionNode(
                parser.take(),
                parser.expecting("of"),
                parser.make.unary_expression()
                )

        return parser.make.exponential_expression()

    def interpret(self):
        pass

    def transpile(self):
        pass
