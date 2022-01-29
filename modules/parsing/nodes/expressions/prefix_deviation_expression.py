from lexing.tokens.operator import Op
from .unary_expression import UnaryExpressionNode

class PrefixDeviationExpressionNode(UnaryExpressionNode):
    @property
    def node_level(self):
        return 2

    @classmethod
    def construct(cls, parser):
        if parser.token.matches_data(Op.INCREMENT, Op.DECREMENT):
            return PrefixDeviationExpressionNode(
                parser.take(),
                parser.make.prefix_deviation_expression()
            )

        return parser.make.postfix_expression()
