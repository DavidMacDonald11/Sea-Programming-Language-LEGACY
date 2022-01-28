from lexing.tokens.keyword import TYPE_KEYWORDS
from lexing.tokens.punctuator import Punc
from ..node import Node

class CastExpressionNode(Node):
    @property
    def cast_type(self):
        return self.components[0]

    @property
    def expression(self):
        return self.components[2]

    def tree_repr(self, depth):
        spacing, down, bottom = self.tree_parts(depth)
        cast_type = f"{spacing}{down}{self.cast_type}"
        expression = f"{spacing}{bottom}{self.expression.tree_repr(depth + 1)}"

        return f"{self.node_name}{cast_type}{expression}"

    @classmethod
    def construct(cls, parser):
        if parser.token.matches_data(*TYPE_KEYWORDS):
            return CastExpressionNode(
                parser.take(),
                parser.expecting(Punc.LPAREN),
                parser.make.cast_expression(),
                parser.expecting(Punc.RPAREN)
            )

        return parser.make.unary_expression()

    def interpret(self):
        pass

    def transpile(self):
        pass
