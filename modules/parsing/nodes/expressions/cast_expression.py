from lexing.tokens.keyword import TYPE_KEYWORDS
from lexing.tokens.punctuator import Punc
from ..node import Node

class CastExpressionNode(Node):
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
